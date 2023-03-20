#NOTE: 
# Run the prefect_gcp_block.py and register the block
# prefect block register --file prefect_gcp_block.py

# spark related packages
import pyspark
from pyspark.sql import SparkSession
#other utility packages
from decouple import config, AutoConfig
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
from datetime import datetime, timedelta
# prefect related packages
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

# Loading Credentials
config = AutoConfig(search_path='.env')
GCS_BUCKET_BLOCK = config("GCS_BUCKET_BLOCK")

@task(retries=3)
def download_data(dataset_url:str, data_folder:str, filename_csv:str): -> Path
    output_dir = Path(data_folder)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f'{datetime.strptime(datetime.today(), "%Y-%m-%d")}_{filename_csv}'
    filepath_local = Path(f'{data_folder}/{filename}')
    # download the csv
    os.system(f"wget {dataset_url} -O {filepath_local}")
    return filepath_local

@task(retries=3)
def write_to_gcs(path:Path) -> None:
    """Loads the dataset into GCS"""
    gcs_block = GcsBucket.load(GCS_BUCKET_BLOCK)
    gcs_block.upload_from_path(from_path=path, to_path=Path(path).as_posix()) # To handle the backslash that is being changed when writing to GCS
    return 

@flow(name='ParentFlow')
def etl_parent_flow() -> None:
    filename = '5cei-gny5'
    data_url = f"https://data.sfgov.org/resource/{filename}.csv"
    data_dir = Path("data_eviction")
    filename_csv ='eviction.csv'


    file_path = download_data(data_url, data_dir, filename_csv)
    #write_to_gcs(file_path)


if __name__=="__main__":
    etl_parent_flow()