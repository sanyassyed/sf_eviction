# Project Setup 

## Start the VM on GCP via CLI - **Step 1**
```bash
# Command to import environment variables in the windows os
source env.bashrc
gcloud compute instances start ${GCP_COMPUTE_ENGINE_NAME} --zone ${GCP_ZONE} --project ${GCP_PROJECT_ID}
# Copy paste the Instance External IP in the ~/.ssh/config file
ssh ${GCP_COMPUTE_ENGINE_NAME}
```

## Instructions to create a project folder and setup version control using GIT 
TODO: Edit and only keep instructions to clone repo using http - **Step 2**
### Creating a repo on the local system and pushing to git
* Create a new folder for the project - sf_eviction
* cd into sf_eviction
* `git init`
* `nano .gitignore` -> add files to be ignored
* `git add .`
* `git commit -m "CICD: Initial Commit"`
* `git remote add origin https://github.com/sanyassyed/sf_eviction.git`
* `git push -u origin master`
* `username: sanyassyed`
* `password <paste_the_personal_access_token_here>` -> you need to create this on the website of github and save the token securely for future use

## Instructions to clone the project repo on a VM and enable pushing and pulling to and from repo respectively

### Connect remote VM to remote git repo via SSH
```bash
   # generate a ssh key pair 
   ssh-keygen -t rsa
   # if you want to give a different name enter the below else press enter
   /home/sanyashireen/.ssh/vm_rsa 
   # add this key to ssh-agent
   # start ssh agent 
   eval `ssh-agent -s`	
   # check if keys are already identified
   ssh-add -l -E sha256
    > The agent has no identities.
   # guide the ssh agent where the keys are stored
   ssh-add /home/sanyashireen/.ssh/vm_rsa
    > Identity added: /home/sanyashireen/.ssh/vm_rsa (sanyashireen@de-zoomcamp)
   # create a `config` file in .ssh folder
   nano config 
   # and write the below to file [Ctrl + O + Enter to save, Ctrl+X to exit]
   # write the path to the key from the root ~ and not /home
    Host github.com
        User git
        IdentityFile ~/.ssh/vm_rsa
   # add the public key to the git account on github.com
   # clone repo as follows using SSH
   git clone git@github.com:sanyassyed/sf_eviction.git
   # check the remote origin is set with ssh
   git remote -v
   # Check the SSH connection with repo from VM using
   ssh -T git@github.com
   # set the global variables
   git config --global user.email "sanya.shireen@gmail.com"
   git config --global user.name "sanya googlevm"
   # make changes in repo
   git add .
   git commit -m "CICD: Initial commit from VM"
   git push -u origin master
   ```

### Goto Project Directory - **Step 3**
```bash
cd sf_eviction
```
## Requirements 
### API
* TODO:

Instructions to install required applications and packages on the VM

### conda 
* TODO:

### Java
* TODO: refer to week 5 de-zoomcamp

### Spark
* TODO: refer to week 5 de-zoomcamp

### Jupyter notebook
* TODO: Check if conda comes with jupyter notebook installed?

## Project environment setup
### Set the virtual conda env
* ` conda create --prefix ./.my_env python=3.10.9 pip` -> Path to install the virtual env in the current project directory with python 3.10 and pip
*  `conda activate .my_env` - to activate the virtual env - **Step 4 Option a**
* `conda activate` -> don't use deactivate just use `activate` to go to base

### Jupyter Notebook with different kernal 

Using jupyter installed on the system and  the kernel from conda virtual env [Ref](https://stackoverflow.com/questions/58068818/how-to-use-jupyter-notebooks-in-a-conda-environment) 

<p> We are going to use the pyhton in the conda virtual env and create a kernal and activate that in the system jupyter notebook </p>

1. Add the conda virtual env python to kernal
    
    ```python
    conda activate .my_env       # activate environment in terminal
    conda/pip install ipykernel  # install Python kernel in new conda env
    ipython kernel install --user --name=conda-myenv-kernel   # configure Jupyter to use Python kernel
    
    # Then run jupyter from the system installation or a different conda environment:
    conda activate               # this step activates the system conda
    jupyter notebook             # run jupyter from system
    ```
    
2. Select the `conda-myenv-kernal` in jupyter notebook form the `New` drop down box

### Start Jupter notebooks **Step 4 Option b**
```bash
conda activate # to goto base conda which has the jupyter installation
screen -A -m -d -S jupyterscreen jupyter notebook --port=8888 # to start jupyter in the background 
# goto the browser and open http://localhost:8888 and select the virtual env kernal
# to stop jupyter notebook
pgrep jupyter
# use the pid printed
kill pid
# activate the project venv
conda activate .my_env/
```

### Installing packages on Conda Virtual env
* `pip install <name_of_the_package>`
* `python-decouple` -> used for setting up and using environment variable within the python code
* `ipykernel` -> to add the virtual conda kernal to the list of kernals available on Jupyter notebook

### Environment Variables for the project

Add environment variables as follows [Ref](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5#:~:text=First%20install%20Python%20Decouple%20into%20your%20local%20Python%20environment.&text=Once%20installed%2C%20create%20a%20.env,to%20add%20your%20environment%20variables.&text=Then%20save%20(WriteOut)%20the%20file,stored%20in%20your%20.env%20file.)

* `pip install python-decouple`
* `touch .env` # create a new .env file
* `nano .env`    # open the .env file in the nano text editor and write the environment variables here
    * Now that you have your environment variables stored in a .env file, you can access them in your Python code like this:
    
        ```python
        from decouple import config, AutoConfig
        config = AutoConfig(search_path='.env')
        API_USERNAME = config('API_USER')
        API_KEY = config('API_KEY')
        ```
    * To specify a different path for .env refer [here](https://stackoverflow.com/questions/43570838/how-do-you-use-python-decouple-to-load-a-env-file-outside-the-expected-paths)

## Project Structure
TODO: later use tree command to copy paste updated structure 
```bash
sf_eviction/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── ...
├── flows/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── ...
├── dbt/
│   ├── analysis/
│   ├── macros/
│   ├── models/
│   ├── snapshots/
│   ├── tests/
│   ├── dbt_project.yml
│   └── ...
├── README.md
└── setup.py
```
## Project Creation
### Prefect
2. Install prefect in the virtual env
    ```bash
    # In a conda environment, install all package dependencies with
    conda activate .my_env/
    pip install -r requirements_prefect.txt
    pip install "prefect-gcp[cloud_storage]"
    ```

3. Use Prefect Cloud [Option 2: the other option is to use the local prefect orion for which you will use `prefect orion start`]
* You must do this step first as the blocks will be created on Prefect Cloud once you log into it using API
    * First Create a Prefect Cloud account
    * Get the API as follows:   
        - To create an API key, select the account icon at the bottom-left corner of the UI and select your account name and the cog-wheel. 
        - This displays your account profile.
        - Select the API Keys tab on the left
        - Select the API Keys tab. This displays a list of previously generated keys and lets you create new API keys or delete keys.
        - Create sf_eviction key and add this data to the .env file as PREFECT_CLOUD_API
    ```bash
    prefect cloud login -k ***PASTE API KEY HERE*****
    ```
    * Now you can use the Prefect cloud to register blocks and run your flows

4. Create Prefect Blocks via code
    * The block creation is done in the file prefect_gcp_block.py
    * In this file we created a GCP Credentials Block - this is to connect to the GCP account
    * And GCS Bucket Block - To access the Buckets in GCS.
    * NOTE: Block names must only contain lowercase letters, numbers, and dashes
    ```bash
    # Run the prefect_gcp_block.py and register the block
    prefect block register --file prefect_gcp_block.py
    ```
    Now for this project we will always connect to the Prefect orion cloud, pull the blocks from there and use it for running our flows.


## Logging out:
```bash
#####Jupyter###
pgrep jupyter
# use the pid printed
kill pid
####Prefect####
prefect cloud logout

```