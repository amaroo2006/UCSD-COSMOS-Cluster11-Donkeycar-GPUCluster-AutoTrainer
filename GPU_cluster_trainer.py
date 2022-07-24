import argparse
import os
import time
import paramiko

from pexpect import *


parser = argparse.ArgumentParser(description = 'Arguments for folders and files')

# local to GPU cluster
parser.add_argument("--data_folder", help="path to folder with driving data that you will transfer to the GPU cluster", required=True)
parser.add_argument("--myconfig_file", help="myconfig file", required=True)


# authentication data
parser.add_argument("--ssh_username", help="your GPU cluster ssh username", required=True)
parser.add_argument("--ssh_password", help="your GPU cluster ssh password", required=True)

# GPU cluster to local
parser.add_argument("--models_folder", help="folder to which you want to save your generated model", required=True)
parser.add_argument("--model_name", help="name of model file to output", required=True)

# process args
args = parser.parse_args()

# get information for ssh
host = "dsmlp-login.ucsd.edu"
password = args.ssh_password
user = args.ssh_username
myConfig = args.myconfig_file
dataFolder = args.data_folder
modelFolder = args.models_folder
modelName = args.model_name


# begin data transfers

print('transferring config file')
myConfigTransfer = "rsync -avr -e ssh {myconfigfile} {username}@dsmlp-login.ucsd.edu:projects/d*_sim/".format(myconfigfile=myConfig, username=user)
run(myConfigTransfer,events={'(?i)password':'{password}\r'.format(password=password)})

print('transferring data folder')
dataTransfer = "rsync -avr -e ssh {dataFolder}/ {username}@dsmlp-login.ucsd.edu:projects/d*_sim/data/".format(dataFolder=dataFolder, username=user)
run(dataTransfer,events={'(?i)password':'{password}\r'.format(password=password)})

print("data transfer done")

# create model
# start ssh process
client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect(hostname=host, username=user, password=password)
print("first connected")
stdin, stdout, stderr = client.exec_command('launch-scipy-ml.sh -g 1 -i ucsdets/ece148-fa19-notebook', get_pty = True)
"""while not stdout.channel.exit_status_ready():
  if stdout.channel.recv_ready():
    stdoutLines = stdout.readlines()
    print(stdoutLines)"""

time.sleep(5)


print("first client started, second started")

client2 = paramiko.SSHClient()
client2.load_system_host_keys()
client2.connect(hostname=host, username=user, password=password)

print("getting pod name")
stdin, stdout, stderr = client2.exec_command('kubectl get pods -o name')
opt = stdout.read()

podName = opt.decode('UTF-8')
podName = podName.strip('\n')
podName = podName[4:]
print(podName)

print("second created")
stdin, stdout, stderr = client2.exec_command('kubectl exec {pod} -- bash -c "cd projects/d*_sim && ls && python train.py --tubs=data/ --model=models/{model}.h5"'.format(pod=podName, model=modelName), get_pty = True)
opt = stdout.readlines()
opt = "".join(opt)
print(opt)

stdin, stdout, stderr = client2.exec_command('kubectl exec -it {pod} -- bash -c exit'.format(pod=podName))
output = stdout.readlines()


modelTransfer = "rsync -avr -e ssh {username}@dsmlp-login.ucsd.edu:projects/d*_sim/models/{modelName}.h5 {resultFolder}/".format(username=user, modelName=modelName, resultFolder=modelFolder)
run(modelTransfer,events={'(?i)password':'{password}\r'.format(password=password)})


stdin.close()
stdout.close()
client.close()
client2.close()
