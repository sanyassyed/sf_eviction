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

## Link the remote VM to sf_eviction remote repo
* `git clone https://github.com/sanyassyed/sf_eviction.git` on the remote VM
* `git add .` -> after making changes
* `git config --global user.email "sanya.shireen@gmail.com"`
* `git config --global user.name "sanya googlevm"`
* `git commit -m "CICD: Updated gitignore from VM"`
* `git push -u origin master` -> after this enter the user name and the personal access token for password
* 