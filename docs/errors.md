Error messages that are related to this project:
* `ModuleNotFoundError: No module named 'pyspark'` -> This happens if you have not activated the virtual env. Therefore perform the following steps
    - set the env variables from env_variables.sh
    - activate virtual env
    - activate base env
    - start jupyter notebook
    - activate virtual env
    - goto the localhost port 8888 to work on the notebooks
    - make sure you have selected the conda-myenv-kernal