## Data Engineering Zoomcamp Capstone Project
---
The goal of this project is to build an end-to-end batch data pipeline to perform ELT on Eviction Data from [DataSF](https://data.sfgov.org/Housing-and-Buildings/Eviction-Notices/5cei-gny5). And execute this task mothly in order to anlyse the eviction patterns from historical data to till date.


## Problem statement
---
* ***Dataset***: 
    The Dataset selected for this project is the `Eviction Notice Dataset of San Francisco` obtained from [DataSF](https://data.sfgov.org/Housing-and-Buildings/Eviction-Notices/5cei-gny5). This data includes eviction notices filed with the San Francisco Rent Board per San Francisco Administrative Code 37.9(c). Notices are published since January 1, 1997. This publshing/update frequency of the dataset is `monthly`. The Data is extracted via Socrate Open Data API (SODA).

* ***Solution***:
    This project aims at extarcting this data from the source via API and building a BATCH ELT which will be scheduled to run monthly and update the connected dashbord for monthly Analytics & Reporting. 


## Data Pipeline 
---
This is a Batch Pipeline which will perform ELT monthly as source data is also updated monthly. The ELT steps include

* Extract dataset from DataSF via API and load the raw data into datalake
* Clean & partition data and load it to datalake 
* Load the Clean & Partitioned Data from datalake into external tables in the datawarehouse
* Transform the data in the data warehouse and prepare it for the dashboard
* Create a dashboard

## Technologies 
---
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
---
![BATCH ELT Architecture](images/architecture.JPG)

Detailed Steps in the ELT:
1. A Project is created on ***GCP*** 
1. SODA API keys and secrets are obtained by creating an account on DataSF, which will be used to extract the data from the source
1. Infrastructure for the Project is created using ***Terraform*** which creates the following:
    * Datalake : ***Google Cloud Storage Bucket*** where the raw and cleaned-partitioned data is stored
    * Data Warehouse: Three Datasets on ***BigQuery*** namely raw, staging and production are created in order to store the tables during different stages of ELT
    * Virtual Machine: A Linux ***Compute Engine*** to schedule and run the pipeline on
1. ***Prefect Cloud API*** is obtained by creating an account
1. The Pilpeline for ELT is created on the VM scheduled for monthly execution and orchestrated via ***Prefect Cloud***; which does the following tasks
    * Extracts raw data from source via ***Socrate Open Data API***
    * Loads raw data to GCS Bucket
    * Cleans and Partitions the raw data using ***Apache Spark***
    * Loads the cleaned and partitoned data as parquet files to GCS
    * Creates External & Non-partitioned tables in the `raw` Dataset in BigQuery by pulling data from GCS. Note: Partitioned or Clustered tables were not created as the dataset produced too many partitions, more than what was allowed in BigQuery. 
    * Transforms Data from BigQuery using ***dbt-core*** and creates views for staging data and fact tables in the dev/prod Dataset along with tests and documentation.
    
    ![dbt-documentation](images/dbt_documentation.JPG)

    ![dbt-lineage](images/dbt_lineage_graph.JPG)

    ![Prefect ETL](images/prefect_flow.JPG)
1. Transformed Data from BigQuery is used for Reporting and Visualization using Looker Studio to produce Dashboards

## Key Findings
---
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


## The Dashboard: 
---

![image](images/report.JPG)

## Reproduction:
---
You can recreate and run the project by following the step by step instructions [here](ProjectReplication.md)

## Conclusion
---
Through this project we were able to successfully build a ELT pipeline end to end which is scheduled to run monthly. And as a result we have a mothly updated list of eviction notices filed in the city of San Francisco which can then be visualized via the Dashboard on Looker Studio. This helps us get some useful insights on the latest eviction trends and patterns.


## Future Work
---
- Combine data about neighbourhoods and districts from other sources and make the reporting more rich.
- Use DataProc to perform Spark job
- Create a normalized data structure when using more data sources