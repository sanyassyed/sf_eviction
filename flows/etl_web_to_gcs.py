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

# spark related packages
import pyspark
from pyspark.sql import SparkSession, types

# Loading Credentials
config = AutoConfig(search_path='.env')
GCS_BUCKET_BLOCK = config("GCS_BUCKET_BLOCK")

@task(retries=3, log_prints=True)
def download_data(source_url:str, data_dir:Path, filename:str) -> Path:
    """ Task to pull raw csv data from the web
    :param dataset_url: data source url
    :param data_folder: local target folder for raw data
    :param raw_filename: raw data filename
    :return: path to raw data downloaded on local system
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    target_path = Path(f'{data_dir}/{filename}')
    # download the csv
    os.system(f"wget {source_url} -O {target_path}")
    return target_path

@task(retries=3, log_prints=True)
def write_to_gcs(path) -> None:
    """Loads the dataset from local system into GCS
    :param path: path to raw data on local system & the path to store the data in on GCS also
    :return: None
    """
    gcs_block = GcsBucket.load(GCS_BUCKET_BLOCK)
    if '.csv' in str(path):
        gcs_block.upload_from_path(from_path=path, to_path=Path(path).as_posix()) # To handle the backslash that is being changed when writing to GCS
    else:
        gcs_block.upload_from_folder(from_folder=path, to_folder=Path(path).as_posix())
    return 

@task(retries=3, log_prints=True)
def clean_data(source_path:Path, data_dir, clean_part_dir:str) -> Path:

    target_dir = f'{data_dir}/{clean_part_dir}'
    spark = SparkSession.builder \
                        .master("local[*]") \
                        .appName('test') \
                        .getOrCreate()
    imp_cols = ['eviction_id', 'address', 'city', 'state', 'zip', 'file_date', 'non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends', 'constraints_date', 'supervisor_district', 'neighborhood', 'client_location']
    schema = types.StructType([
                                types.StructField('eviction_id', types.StringType(), True), 
                                types.StructField('address', types.StringType(), True), 
                                types.StructField('city', types.StringType(), True), 
                                types.StructField('state', types.StringType(), True), 
                                types.StructField('zip', types.IntegerType(), True), 
                                types.StructField('file_date', types.DateType(), True), 
                                types.StructField('non_payment', types.BooleanType(), True), 
                                types.StructField('breach', types.BooleanType(), True), 
                                types.StructField('nuisance', types.BooleanType(), True), 
                                types.StructField('illegal_use', types.BooleanType(), True), 
                                types.StructField('failure_to_sign_renewal', types.BooleanType(), True), 
                                types.StructField('access_denial', types.BooleanType(), True), 
                                types.StructField('unapproved_subtenant', types.BooleanType(), True), 
                                types.StructField('owner_move_in', types.BooleanType(), True), 
                                types.StructField('demolition', types.BooleanType(), True), 
                                types.StructField('capital_improvement', types.BooleanType(), True), 
                                types.StructField('substantial_rehab', types.BooleanType(), True), 
                                types.StructField('ellis_act_withdrawal', types.BooleanType(), True), 
                                types.StructField('condo_conversion', types.BooleanType(), True), 
                                types.StructField('roommate_same_unit', types.BooleanType(), True), 
                                types.StructField('other_cause', types.BooleanType(), True), 
                                types.StructField('late_payments', types.BooleanType(), True), 
                                types.StructField('lead_remediation', types.BooleanType(), True), 
                                types.StructField('development', types.BooleanType(), True), 
                                types.StructField('good_samaritan_ends', types.BooleanType(), True), 
                                types.StructField('constraints_date', types.StringType(), True), 
                                types.StructField('supervisor_district', types.IntegerType(), True), 
                                types.StructField('neighborhood', types.StringType(), True), 
                                types.StructField('client_location', types.StringType(), True)])

    df = spark.read \
              .option("header", "true") \
              .schema(schema) \
              .csv(str(source_path)) \
              .select(imp_cols)
    
    print(f'Total rows read: {df.count()}')
    df = df.repartition(2) #TODO: MAybe call the write_to_gcs for each item in the folder? as getting a WARNING | urllib3.connectionpool - Connection pool is full, discarding connection: storage.googleapis.com. Connection pool size: 10
    df.write.parquet(target_dir, mode='overwrite')
    spark.stop()
    return target_dir


# TODO:
# Read raw data from GCS into pandas df [Iteration 2 -Pyspark df]
# Clean it write to GCS clean_eviction.parquet
# Write 1) external table to bq and 2)create partition table from it

@flow(name='ParentFlow')
def etl_parent_flow(dataset_name:str, filename_o:str) -> None:
    """
    Main flow that calls the tasks
    :param dataset_name: the source dataset name
    :param filename_o: the target filename which will be used for storing the data
    :return:
    """
    data_url = f"https://data.sfgov.org/resource/{dataset_name}.csv"
    time = datetime.now()
    year = time.year
    month = time.month
    day = time.day
    data_prefix =['raw', 'clean', 'clean_partitioned']
    data_dir = Path(f"data_{filename_o}/{year}/{month}/{day}")
    # this will later get the prefix raw, clean or clean_partitioned
    filename = f'{filename_o}_{time.strftime("%Y-%m-%d")}'

    # 1 - To download raw data to VM -> download_data(data_url, data_dir, filename)
    # 2 - To write raw data VM to GCS -> write_to_gcs(filepath_raw)
    # 3 - To clean raw data and write to VM -> clean_data(filepath_raw)
    # 4 - To write clean data VM to BQ as external table -> write_to_bq(filepath_clean)
    # 5 - To write clean data VM to GCS (Reuse 2?) -> write_to_gcs(filepath_clean)
    
    raw_filename = f'{data_prefix[0]}_{filename}.csv'
    #clean_data_dir = f'{data_prefix[1]}_{filename}'
    clean_part_data_dir = f'{data_prefix[2]}_{filename}' # Note: if wanting to partition data 


    raw_filepath = download_data(data_url, data_dir, raw_filename)
    write_to_gcs(raw_filepath)
    #clean_datapath = clean_data(raw_filepath, data_dir, clean_data_dir)
    clean_datapath = clean_data(raw_filepath, data_dir, clean_part_data_dir)
    write_to_gcs(clean_datapath)
    
    # testing
    # gcs_data_path = 'data_eviction/2023/3/22/gcs_raw_eviction_2023-03-22.csv'
    # pq_parti_data_dir = 



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