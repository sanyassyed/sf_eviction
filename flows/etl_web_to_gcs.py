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
import pyspark
from pyspark.sql import SparkSession

# other utility packages
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

@task(retries=3, log_prints=True)
def download_data(dataset_url:str, data_dir:Path, filename:str) -> Path:
    """ Task to pull raw csv data from the web
    :param dataset_url: data source url
    :param data_folder: local target folder for raw data
    :param raw_filename: raw data filename
    :return: path to raw data downloaded on local system
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    filename_raw = f'web_raw_{filename}.csv'
    filepath_raw = Path(f'{data_dir}/{filename_raw}')
    # download the csv
    os.system(f"wget {dataset_url} -O {filepath_raw}")
    return filepath_raw

@task(retries=3, log_prints=True)
def write_to_gcs(path:Path) -> None:
    """Loads the dataset from local system into GCS
    :param path: path to raw data on local system & the path to store the data in on GCS also
    :return: None
    """
    gcs_block = GcsBucket.load(GCS_BUCKET_BLOCK)
    gcs_block.upload_from_path(from_path=path, to_path=Path(path).as_posix()) # To handle the backslash that is being changed when writing to GCS
    return 

@task(retries=3, log_prints=True)
def pull_from_gcs(filepath_raw:Path, data_dir:Path, filename:str)-> pyspark.sql.dataframe.DataFrame:
    """Ref: https://prefecthq.github.io/prefect-gcp/examples_catalog/#cloud-storage-module"""
    path_source = Path(filepath_raw).as_posix()
    path_target = Path(f'{data_dir}/gcs_raw_{filename}.csv')
    gcs_block = GcsBucket.load(GCS_BUCKET_BLOCK)
    gcs_block.download_object_to_path(from_path=path_source, to_path=path_target)
    return path_target

@task(retries=3, log_prints=True)
def write_as_parquet(raw_data_filepath:Path, data_dir:Path, filename:str, data_state:str)-> pyspark.sql.dataframe.DataFrame:
    """reads csv data and writes it as parquet"""
    spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
    
    df = spark.read.option("header", "true").csv(str(raw_data_filepath))
    df = df.repartition(100)
    # folder to write the partition into
    data_partition_dir = f'{data_dir}/{data_state}_{filename}_partitioned'
    # to ALLOW overwriting use this
    # writing the PySpark DF as a parquet file after changing the schema
    df.write.parquet(f'{data_partition_dir}/', mode='overwrite')


    spark.stop()
    print('\n\n spark task done! \n\n')
    return data_partition_dir


# TODO:
# Read raw data from GCS into pandas df [Iteration 2 -Pyspark df]
# Clean it write to GCS clean_eviction.parquet
# Write 1) external table to bq and 2)create partition table from it

@flow(name='ParentFlow')
def etl_parent_flow(dataset_name:str, filename_o:str) -> None:
    """
    Main flow that calls the tasks
    :param dataset_name: the source dataset name
    :param filename: the target filename which will be used for storing the data
    :return:
    """
    data_url = f"https://data.sfgov.org/resource/{dataset_name}.csv"
    time = datetime.now()
    year = time.year
    month = time.month
    day = time.day
    data_state =['raw', 'clean']
    data_dir = Path(f"data_{filename_o}/{year}/{month}/{day}")
    filename = f'{filename_o}_{time.strftime("%Y-%m-%d")}'

    # 1 - To download raw data to VM -> download_data(data_url, data_dir, filename)
    # 2 - To write raw data VM to GCS -> write_to_gcs(filepath_raw)
    # 3 - To clean raw data and write to VM -> clean_data(filepath_raw)
    # 4 - To write clean data VM to BQ as external table -> write_to_bq(filepath_clean)
    # 5 - To write clean data VM to GCS (Reuse 2?) -> write_to_gcs(filepath_clean)
    
    filepath_raw = download_data(data_url, data_dir, filename)
    write_to_gcs(filepath_raw)
    gcs_data_path = pull_from_gcs(filepath_raw, data_dir, filename)
    
    # testing
    # gcs_data_path = 'data_eviction/2023/3/22/gcs_raw_eviction_2023-03-22.csv'
    # pq_parti_data_dir = 
    
    pq_parti_data_dir = write_as_parquet(gcs_data_path, data_dir, filename, data_state[0])
    print(pq_parti_data_dir)



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