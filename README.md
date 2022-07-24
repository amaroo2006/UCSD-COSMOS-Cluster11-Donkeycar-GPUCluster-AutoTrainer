# UCSD-COSMOS-Cluster11-Donkeycar-GPUCluster-AutoTrainer
Python script that syncs driving data from your virtual machine to the GPU cluster, trains a model, and transfers the model back to your virtual machine

### Usage
Activate anaconda environment in your virtual machine: 
```
conda activate donkey
```
#### Installing required python packages:
```
pip install paramiko
pip install argparse
```

#### Navigate to d4_sim directory
```
cd projects/d4_sim/
```

#### Clone repository and move python file to d4_sim folder
```
git clone https://github.com/amaroo2006/UCSD-COSMOS-Cluster11-Donkeycar-GPUCluster-AutoTrainer.git
cd UCSD-COSMOS-Cluster11-Donkeycar-GPUCluster-AutoTrainer/
mv GPU_cluster_trainer.py ../
cd ..
rm -rf UCSD-COSMOS-Cluster11-Donkeycar-GPUCluster-AutoTrainer/
```
### Running the script
Use ```python GPU_cluster_trainer.py -h``` to view the command line arguments and their usage

There are 6 command line arguments, all of which are required:

```
--data_folder: path to folder with driving data that you will transfer to the GPU cluster
--myconfig_file: myconfig file you want to copy to the GPU cluster 
--ssh_username: your GPU cluster ssh username
--ssh_password: your GPU cluster ssh password
--models_folder: folder to which you want to save your generated model
--model_name: name of model file to output
```


Running the script with example arguments: 
```
python GPU_cluster_trainer.py --data_folder data/ --myconfig_file myconfig.py --ssh_username exampleUsername --ssh_password examplePassword --models_folder models/ --model_name test_model.h5
```

After the program prints "second started" in the virtual machine's terminal, the model is being created. Just wait and it should finish after a while(time depends on dataset size).


After the script finishes running, your model should be saved to the models folder you specified in the command line arguments. 

