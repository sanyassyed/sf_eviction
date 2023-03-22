# Project Plan
## Steps
1. [ ] Setup Infrastructure using Terraform
1. [X] Pull data from the source -> `Python`-> `Prefect`
    * [X] via wget
    * [ ] via requets/HttpHook package functions
2. [ ] Option 1: Save the RAW data as ~~parquet~~ csv file -> `Python`-> `Prefect`
    * [X] Locally in the data folder for testing / testing folder in `GoogleCloudStorage GCS`?
    * [X] On `GCS` ? -> `Prefect Blocks`
2. [X] Read data from local or `GCS` into pyspark DF -> `Python` -> `Spark` -> `Prefect` 
2. [ ] Option 2: Save the RAW data as PARTITIONED parquet files -> `Python` -> `Spark` -> `Prefect`
    * [X] Locally in the data folder [for testing?]  
    * [ ] ~~On `GCS`~~ ? Would lead to repetition, best to save partitioned data after cleaning
3. [ ] Transform the data by applying schema i.e. fix data types, handle null values, remove uninteresting data etc -> `Python` -> `Spark` -> `Prefect`
3. [ ] Save the TRANSFORMED data as partitioned - parquet files on `GCS` -> `Python` -> `Spark` -> `Prefect`
4. [ ] Load Data from `GCS` into BQ to create external tables -> `Prefect Blocks`?
5. [ ] From external table create partitioned tables ? **[Did this manually using the Query editor in BQ]** Try doing this using Prefect & Spark? (Look at Hint 1)
5. [ ] Using DBT transform - pull data from bq partitioned tables and create fact tables -> `dbt` -> `Piperider` ?
4. [ ] Pull data from fact table and make visualizations -> `Looker`

## TODO:
* Setup scheduling, maybe mothly?
* How will the new data be saved? Appended or Updated?


Technologies:
- > `Prefect`
- > `Docker`
- > `Spark`
- > `BigQuery`
- > `GoogleCloudStorage`
- > `dbt`
- > `Looker`
- > `Python`