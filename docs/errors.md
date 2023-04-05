Error messages that are related to this project:
* `ModuleNotFoundError: No module named 'pyspark'` -> This happens if you have not activated the virtual env. Therefore perform the following steps
    - set the env variables from env_variables.sh
    - activate virtual env
    - activate base env
    - start jupyter notebook
    - activate virtual env
    - goto the localhost port 8888 to work on the notebooks
    - make sure you have selected the conda-myenv-kernal
* `WARNING | urllib3.connectionpool - Connection pool is full, discarding connection: storage.googleapis.com. Connection pool size: 10`
    - reduce partition size -TRIED
    - or maybe call the write_to_gcs for each item in the folder? as getting a -NOT TRIED

* `Too many partitions produced by query, allowed 4000, query produces at least 6389 partitions`
    - Error in BQ when trying to create a partition table based on file_date
* Unable to assign environment variable to local variables in dbt_profile.yml 
    - They can only be used elsewhere in yml files but not to assign values via `vars`
    - Hence I've assigned the values in the schema.yml & stg_eviction.sql directly from the env variables using `env_var()` function instead of `var()` function