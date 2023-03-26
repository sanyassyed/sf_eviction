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
from pyspark.sql import SparkSession, types

# other utility packages
from decouple import config, AutoConfig
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
import json

# prefect related packages
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket

# Loading Credentials
config = AutoConfig(search_path='.env')
GCS_BUCKET_BLOCK = config("GCS_BUCKET_BLOCK")
# SODU API Credentials
API_TOKEN = config("API_TOKEN")
API_KEY_ID = config("API_KEY_ID")
API_KEY_SECRET = config("API_KEY_SECRET")

@task(log_prints=True)
def get_json(endpoint, headers):
    """download the json by supplying the api token in the header"""
    headers['Accept'] = 'application/json' # csv?
    # pull_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%dT%H:%M:%S") # year, month, day, hour, minute, seconds, microseconds
    combined = []
    params = f"""$query=SELECT:*,* ORDER BY :id LIMIT 200000"""
    # response has two parts .json() and .headers https://www.w3schools.com/python/ref_requests_response.asp
    response = requests.get(endpoint, headers=headers, params=params)
    captured = response.json()
    combined.extend(captured)
    print('get_json complete')
    return combined

@task(retries=3, log_prints=True)
def write_to_local(content:list, data_dir:Path, filename:str) -> Path:
    """ Task to pull raw csv data from the web
    :param dataset_url: data source url
    :param data_folder: local target folder for raw data
    :param raw_filename: raw data filename
    :return: path to raw data downloaded on local system
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    target_path = Path(f'{data_dir}/{filename}')
    # download the csv
    data_json = json.dumps(content, indent=4)
    open(target_path,"w", encoding='utf8').write(data_json)
    return target_path

@task(retries=3, log_prints=True)
def write_to_gcs(path) -> None:
    """Loads the dataset from local system into GCS
    :param path: path to raw data on local system & the path to store the data in on GCS also
    :return: None
    """
    gcs_block = GcsBucket.load(GCS_BUCKET_BLOCK)
    if '.json' in str(path):
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
    imp_cols = ['eviction_id', 'address', 'city', 'state', 'zip', 'file_date', 'non_payment', 'breach', 'nuisance', 'illegal_use', 'failure_to_sign_renewal', 'access_denial', 'unapproved_subtenant', 'owner_move_in', 'demolition', 'capital_improvement', 'substantial_rehab', 'ellis_act_withdrawal', 'condo_conversion', 'roommate_same_unit', 'other_cause', 'late_payments', 'lead_remediation', 'development', 'good_samaritan_ends', 'constraints_date', 'supervisor_district', 'neighborhood', 'client_location', ':created_at', ':updated_at']
    schema = types.StructType([
        types.StructField(':@computed_region_26cr_cadq', types.StringType(), True), 
        types.StructField(':@computed_region_6ezc_tdp2', types.StringType(), True), 
        types.StructField(':@computed_region_6pnf_4xz7', types.StringType(), True), 
        types.StructField(':@computed_region_6qbp_sg9q', types.StringType(), True), 
        types.StructField(':@computed_region_9jxd_iqea', types.StringType(), True), 
        types.StructField(':@computed_region_ajp5_b2md', types.StringType(), True), 
        types.StructField(':@computed_region_bh8s_q3mv', types.StringType(), True), 
        types.StructField(':@computed_region_fyvs_ahh9', types.StringType(), True), 
        types.StructField(':@computed_region_h4ep_8xdi', types.StringType(), True), 
        types.StructField(':@computed_region_jwn9_ihcz', types.StringType(), True), 
        types.StructField(':@computed_region_p5aj_wyqh', types.StringType(), True), 
        types.StructField(':@computed_region_pigm_ib2e', types.StringType(), True), 
        types.StructField(':@computed_region_qgnn_b9vv', types.StringType(), True), 
        types.StructField(':@computed_region_rxqg_mtj9', types.StringType(), True), 
        types.StructField(':@computed_region_yftq_j783', types.StringType(), True), 
        types.StructField(':created_at', types.TimestampType(), True), 
        types.StructField(':id', types.StringType(), True), 
        types.StructField(':updated_at', types.TimestampType(), True), 
        types.StructField(':version', types.StringType(), True), 
        types.StructField('access_denial', types.BooleanType(), True), 
        types.StructField('address', types.StringType(), True), 
        types.StructField('breach', types.BooleanType(), True), 
        types.StructField('capital_improvement', types.BooleanType(), True), 
        types.StructField('city', types.StringType(), True), 
        types.StructField('client_location', types.MapType(types.StringType(), types.StringType(), True), True), 
        types.StructField('condo_conversion', types.BooleanType(), True), 
        types.StructField('constraints_date', types.StringType(), True), 
        types.StructField('demolition', types.BooleanType(), True), 
        types.StructField('development', types.BooleanType(), True), 
        types.StructField('ellis_act_withdrawal', types.BooleanType(), True), 
        types.StructField('eviction_id', types.StringType(), True), 
        types.StructField('failure_to_sign_renewal', types.BooleanType(), True), 
        types.StructField('file_date', types.DateType(), True), 
        types.StructField('good_samaritan_ends', types.BooleanType(), True), 
        types.StructField('illegal_use', types.BooleanType(), True), 
        types.StructField('late_payments', types.BooleanType(), True), 
        types.StructField('lead_remediation', types.BooleanType(), True), 
        types.StructField('neighborhood', types.StringType(), True), 
        types.StructField('non_payment', types.BooleanType(), True), 
        types.StructField('nuisance', types.BooleanType(), True), 
        types.StructField('other_cause', types.BooleanType(), True), 
        types.StructField('owner_move_in', types.BooleanType(), True), 
        types.StructField('roommate_same_unit', types.BooleanType(), True), 
        types.StructField('shape', types.StructType([
            types.StructField('coordinates', types.ArrayType(types.DoubleType(), True), True), 
            types.StructField('type', types.StringType(), True)]), True), 
        types.StructField('state', types.StringType(), True), 
        types.StructField('substantial_rehab', types.BooleanType(), True), 
        types.StructField('supervisor_district', types.StringType(), True), 
        types.StructField('unapproved_subtenant', types.BooleanType(), True), 
        types.StructField('zip', types.StringType(), True)])

    df = spark.read \
            .option("multiline","true") \
            .schema(schema) \
            .json(str(source_path)) \
            .select(imp_cols) \
            .withColumnRenamed(':updated_at', 'updated_at') \
            .withColumnRenamed(':created_at', 'created_at') 
    print(f'Total rows read: {df.count()}')
    df = df.withColumn("latitude", df["client_location"].getItem("latitude").cast("double")) \
        .withColumn("longitude", df["client_location"].getItem("longitude").cast("double")) \
        .drop("client_location")

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
    SODA_url = f"https://data.sfgov.org/resource/{dataset_name}"
    SODA_headers = {
    'keyId': API_KEY_ID,
    'keySecret': API_KEY_SECRET
    }

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
    
    raw_filename = f'{data_prefix[0]}_{filename}.json'
    #clean_data_dir = f'{data_prefix[1]}_{filename}'
    clean_part_data_dir = f'{data_prefix[2]}_{filename}' # Note: if wanting to partition data 

    
    content = get_json(SODA_url, SODA_headers)
    raw_filepath = write_to_local(content, data_dir, raw_filename)
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