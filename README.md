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
    Host sanyassyed.github.com
        HostName github.com
        PreferredAuthentications publickey
        IdentityFile /home/sanyashireen/.ssh/vm_rsa
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