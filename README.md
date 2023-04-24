## Course Project

The goal of this project is to build an end-to-end batch data pipeline to extract Eviction Data from [DataSF](https://data.sfgov.org/Housing-and-Buildings/Eviction-Notices/5cei-gny5) mothly to anlyse the eviction patterns from historical data till date.


### Problem statement

* ***Dataset***: 
    The Dataset selected for this project is the `Eviction Notice Dataset of San Francisco` obtained from [DataSF](https://data.sfgov.org/Housing-and-Buildings/Eviction-Notices/5cei-gny5). This data includes eviction notices filed with the San Francisco Rent Board per San Francisco Administrative Code 37.9(c). Notices are published since January 1, 1997. This publshing/update frequency of the dataset is `monthly`. The Data is extracted via Socrate Open Data API (SODA).

* ***Solution***:
    This project aims at extarcting this data from the source via API and building a BATCH ELT which will be scheduled to run monthly and update the connected dashbord for monthly Analytics & Reporting. 


## Data Pipeline 

This is a Batch Pipeline which will perform ELT monthly as the data at the spource is also updated monthly. The ELT steps include

* Extract dataset from DataSF via API load the raw data into datalake (GCS)
* Clean & partition data and load it to datalake 
* Load the Clean & Partitioned Data from datalake into external tables in the datawarehouse
* Transform the data in the data warehouse: prepare it for the dashboard
* Create a dashboard

## Technologies 

* Cloud: GCP
* Infrastructure as code (IaC): Terraform
* Workflow orchestration: Prefect
* Data Wareshouse: BigQuery
* Batch processing: Spark
* Data Transformation: dbt-core
* Dashboard: Looker Studio
* Software Building Automation Tool: Make
* Virtual Environment: Anaconda
* CICD: Git

## Architecture

![BATCH ELT Architecture](images/architecture.JPG)

Detailed Steps in the ELT:
1. A Project is created on GCP 
1. SODA API keys and secrets are obtained by creating an account on DataSF to pull the data from the source
1. Infrastructure for the Project is created using Terraform which creates the following:
    * Datalake : Google Cloud Storage Bucket
    * Data Warehouse: Three Datasets on Bigquery namely raw, staging and production to store the tables during different stages of ELT
    * Virtual Machine: A Linux Compute Engine to schedule and run the pipeline on
1. Prefect Cloud API is obtained by creating an account
1. The Pilpeline for ELT is created on the VM which is scheduled for monthly execution and orchestrated via Prefect Cloud which does the following tasks
    * Extracts raw data from source via API
    * Loads raw data to GCS Bucket
    * Cleans and Partitions the raw data using Apache Spark
    * Loads the cleaned and partitoned data as parquet files to GCS
    * Creates tables in BigQuery by pulling data from GCS
    * Transforms Data from BigQuery using dbt-core and creates views and fact tables in the Production/Development Dataset
1. Transformed Data from BigQuery is used for Reporting and Visualization using Looker Studio to produce Dashboards

## Key Findings
In the dashboard the data from BigQuery is blended with [Supervisor Dataset](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Supervisor-Districts-2022-/f2zs-jevy/data?no_mobile=true) on Looker Studio to develop Visualizations in order to answer some key questions.

The dashboard is accessible from [here](https://lookerstudio.google.com/reporting/688e19ba-3476-45f2-9dba-94d813bb9328)

The questions that were aimed to answer and the corresponding findings are as below:

1. What has been the trend of overall evictions over the years in San Francisco?

    The trend has been cyclical co-relating with the economic outlook in the city but overall it has been trending downwards with a maximum of 2897 evictions in 1998 to a low of 778 evictions in 2020.

1. What is the most recorded reason for eviction? 

    Looking at the heatmap, it is evident that ***Owner Movein*** has been the most recorded reason for eviction. But in recent years, this reason for eviction has become ***Nuisance***

1. Over the years, what has been the least recorded reason for eviction?

    Over the years that data has been available, the least number of recorded reason for eviction has been for ***Lead Remediation*** 


1. What are the top 3 reasons for eviction recorded over the last 10 years?
    
    The top 3 reasons are 
    - Breach of contract
    - Nuisance 
    - Owner movein

1. Which neighbourhood has seen the most evictions in 2022?

    The neighbourhood which saw most evictions is ***Financial Distriction/South Beach***

1. Which neighbourhood has seen the lowest evictions in 2022?

    The neighbourhood which saw lowest evictions is ***Mission Bay***. 


1. Which supervisor has the most challenges w.r.t evictions in SF in 2022?
    
    Supervisor ***Matt Dorsey*** had the most number of evictions to deal with . This data could be utilized to ensure that the teams are sized right in the respective districts. 

1. Looking at the trend of data, what would be your recommendation in the way that data is recorded?
    
    Given the trend of data, that ***Nusiance*** and ***Breach*** numbers have been increasing, the recommendation would be to break down these 2 reasons to better understand the exact reasons. This will allow the city council to take targeted actions to address this concern. 


The Dashboard: 

![image](images/report.JPG)


## Peer review criteria

* Problem description
    * 0 points: Problem is not described
    * 1 point: Problem is described but shortly or not clearly 
    * 2 points: Problem is well described and it's clear what the problem the project solves
* Cloud
    * 0 points: Cloud is not used, things run only locally
    * 2 points: The project is developed in the cloud
    * 4 points: The project is developed in the cloud and IaC tools are used
* Data ingestion (choose either batch or stream)
    * Batch / Workflow orchestration
        * 0 points: No workflow orchestration
        * 2 points: Partial workflow orchestration: some steps are orchestrated, some run manually
        * 4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake
    * Stream
        * 0 points: No streaming system (like Kafka, Pulsar, etc)
        * 2 points: A simple pipeline with one consumer and one producer
        * 4 points: Using consumer/producers and streaming technologies (like Kafka streaming, Spark streaming, Flink, etc)
* Data warehouse
    * 0 points: No DWH is used
    * 2 points: Tables are created in DWH, but not optimized
    * 4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)
* Transformations (dbt, spark, etc)
    * 0 points: No tranformations
    * 2 points: Simple SQL transformation (no dbt or similar tools)
    * 4 points: Tranformations are defined with dbt, Spark or similar technologies
* Dashboard
    * 0 points: No dashboard
    * 2 points: A dashboard with 1 tile
    * 4 points: A dashboard with 2 tiles
* Reproducibility
    * 0 points: No instructions how to run code at all
    * 2 points: Some instructions are there, but they are not complete
    * 4 points: Instructions are clear, it's easy to run the code, and the code works


## Going the extra mile 

If you finish the project and you want to improve it, here are a few things you can do:

* Add tests
* Use make
* Add CI/CD pipeline 

This is not covered in the course and this is entirely optional.

If you plan to use this project as your portfolio project, it'll 
definitely help you to stand out from others.

> **Note**: this part will not be graded. 
