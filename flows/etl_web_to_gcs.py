# -- coding: utf-8 --
""" 
Description: Flows and Tasks that perform ELT
Behaviour: 
- Pulls raw data from the web
- Stores on VM locally
- Writes Raw data to GCS
NOTE: 
Run the `create_prefect_blocks.py` and register the block as follows
`prefect block register --file create_prefect_blocks.py`
"""

# spark related packages
# import pyspark
# from pyspark.sql import SparkSession
#other utility packages
from decouple import config, AutoConfig
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
# prefect related packages
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket

# Loading Credentials
config = AutoConfig(search_path='.env')
GCS_BUCKET_BLOCK = config("GCS_BUCKET_BLOCK")

@task(log_prints=True, tags=["extract"], cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def download_data(dataset_url:str, data_folder:str, raw_filename:str) -> Path:
    """ Task to pull raw csv data from the web
    :param dataset_url: data source url
    :param data_folder: local target folder for raw data
    :param raw_filename: raw data filename
    :return: path to raw data downloaded on local system
    """

    output_dir = Path(data_folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f'{datetime.now().strftime("%Y-%m-%d")}_{raw_filename}'
    filepath_local = Path(f'{data_folder}/{filename}')
    # download the csv
    os.system(f"wget {dataset_url} -O {filepath_local}")
    return filepath_local

@task(retries=3)
def write_to_gcs(path:Path) -> None:
    """Loads the dataset from local system into GCS
    :param path: path to raw data on local system & the path to store the data in on GCS also
    :return: None
    """
    gcs_block = GcsBucket.load(GCS_BUCKET_BLOCK)
    gcs_block.upload_from_path(from_path=path, to_path=Path(path).as_posix()) # To handle the backslash that is being changed when writing to GCS
    return 

@flow(name='ParentFlow')
def etl_parent_flow(dataset_name:str, filename:str) -> None:
    """
    Main flow that calls the tasks
    :param dataset_name: the source dataset name
    :param filename: the target filename which will be used for storing the data
    :return:
    """
    data_url = f"https://data.sfgov.org/resource/{dataset_name}.csv"
    data_dir = Path(f"data_{filename}")
    raw_filename = f'raw_{filename}.csv'
    file_path = download_data(data_url, data_dir, raw_filename)
    write_to_gcs(file_path)

# TODO:
# Read raw data from GCS into pandas df [Iteration 2 -Pyspark df]
# Clean it write to GCS clean_eviction.parquet
# Write 1) external table to bq and 2)create partition table from it

if __name__=="__main__":
    """
    Main function that calls the parent flow with the source dataset name and the target filename
    """
    dataset_name = '5cei-gny5'
    filename ='eviction'
    etl_parent_flow(dataset_name, filename)

# Run as follows:
# conda activate .my_env/
# source env_variables.sh
# prefect cloud login -k $PREFECT_CLOUD_API
# python flows/etl_web_to_gcs.py