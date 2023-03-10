# Project Setup 

## Instructions to create a project folder and setup version control using GIT 

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
## Instructions to install required applications and packages on the VM

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
*  `conda activate .my_env` - to activate the virtual env
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

