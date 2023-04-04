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
from prefect_gcp.bigquery import BigQueryWarehouse

# Loading Credentials
config = AutoConfig(search_path='.env')
GCS_BUCKET_BLOCK = config("GCS_BUCKET_BLOCK")
BQ_BLOCK = config("BQ_BLOCK")
GCP_PROJECT_ID = config("GCP_PROJECT_ID")
GCS_BUCKET = config("GCS_BUCKET")

# SODU API Credentials
API_KEY_ID = config("API_KEY_ID")
API_KEY_SECRET = config("API_KEY_SECRET")

@task(log_prints=True)
def get_json(endpoint, headers) -> list:
    """Task to download raw data in json format by supplying the api token in the HTTPS header along with parameters
    param endpoint: url of the source data
    param headers: dictionary containing the API key and secret
    return: the data extraced from the source as a list of dictionaries
    """
    headers['Accept'] = 'application/json'
    combined = []
    params = f"""$query=SELECT:*,* ORDER BY :id LIMIT 200000"""
    response = requests.get(endpoint, headers=headers, params=params)
    captured = response.json()
    combined.extend(captured)
    print(f'LOGGING: Json data extraction from source COMPLETE')
    return combined

@task(retries=3, log_prints=True)
def write_to_local(content:list, data_dir:Path, filename:str) -> Path:
    """ Task to write raw data to VM as json file
    :param content: data (list of dictionaries) pulled from the source
    :param data_dir: path to the local data directory where filename will be saved 
    :param filename: file name for raw data
    :return: path to the raw data file
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    target_path = Path(f'{data_dir}/{filename}')
    
    # write json to local
    import json
    out_file = open(target_path,"w", encoding='utf8')
    json.dump(content, out_file, indent=4)
    out_file.close()
    print(f'LOGGING: Raw data written to path {target_path} COMPLETE')
    return target_path

@task(retries=3, log_prints=True)
def write_to_gcs(path) -> None:
    """Task to load the data from local system into GCS
    :param path: path to raw/clean data on local system & the same path is also used to store the data on GCS
    :return: None
    """
    gcs_block = GcsBucket.load(GCS_BUCKET_BLOCK)
    if '.json' in str(path):
        gcs_block.upload_from_path(from_path=path, to_path=Path(path).as_posix()) # To handle the backslash that is being changed when writing to GCS
    else:
        gcs_block.upload_from_folder(from_folder=path, to_folder=Path(path).as_posix())
    print(f"LOGGING: Write to GSC bucket path: {path} COMPLETE")
    return 

@task(log_prints=True)
def clean_data(source_path:Path, data_dir, clean_part_dir:str) -> Path:
    """ Task to clean raw data and write as partitioned parquet files to the local system(VM)
    :param source_path: path to raw data on local system
    :param data_dir: path to the local data directory where clean_part_dir will be saved 
    :param clean_part_dir: name of the directory where clean partitioned parquet files will be written
    :return: path to clean data on the local system(VM)
    """    
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
    print(f'LOGGING: Total rows read: {df.count()}')
    df = df.withColumn("latitude", df["client_location"].getItem("latitude").cast("double")) \
        .withColumn("longitude", df["client_location"].getItem("longitude").cast("double")) \
        .drop("client_location")

    df = df.repartition(2) 
    df.write.parquet(target_dir, mode='overwrite')
    spark.stop()
    print(f'Clean data written to path {target_dir} COMPLETE')
    return target_dir

@task(log_prints=True, retries=3)
def write_to_bq(bq_dataset_name:str, bq_table_name_external:str, bq_table_name:str, clean_datapath:str) -> None:
    """ Task to: 
        1)create external table in BQ with clean data uploaded to GCS & 
        2)create non-partitioned table from the external table just created
    :param bq_dataset_name: the name of the dataset on BQ
    :param bq_table_name_external: name to give the external table being created
    :param bq_table_name: name to give to the non-partition table being created
    :param clean_datapath: path to the folder where the clean partitioned data is stored on GCS
    :return: None
    """    
    external_table = f'{GCP_PROJECT_ID}.{bq_dataset_name}.{bq_table_name_external}'
    table = f'{GCP_PROJECT_ID}.{bq_dataset_name}.{bq_table_name}'
    
    query_external_table = f'''
    CREATE OR REPLACE EXTERNAL TABLE `{external_table}`
    OPTIONS (
    format = 'parquet',
    uris = ['gs://{GCS_BUCKET}/{clean_datapath}/*.parquet']);
    '''
    # not creating partition table as no datetime column available

    query_table = f'''
    CREATE OR REPLACE TABLE `{table}`
    AS
    SELECT * FROM `{external_table}`;
    '''

    with BigQueryWarehouse.load(BQ_BLOCK) as warehouse:
        warehouse.execute(query_external_table)
        print(f'LOGGING: External table {external_table} creation COMPLETE')
        warehouse.execute(query_table)
        print(f'LOGGING: Non-partition table {table} creation COMPLETE')

@flow(name='WriteToGCSSubFlow', log_prints=True)
def write_to_gcs_subflow(path) -> None:
    """
    Sub flow that calls the task to write to GCS
    :param path: path to raw/clean data on local system & the same path is also used to store the data on GCS
    :return: None
    """
    write_to_gcs(path)

@flow(name='ParentFlow', log_prints=True)
def etl_parent_flow(dataset_name:str, filename_o:str) -> None:
    """
    Main flow that calls the tasks
    :param dataset_name: the source dataset name being extracted from the sf website
    :param filename_o: the target filename/and table name in bq which will be used for storing the data
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
    data_dir = Path(f"data_{filename_o}/{year}/{month}/{day}") # folder to save raw and clean data locally on the VM
    filename = f'{filename_o}_{time.strftime("%Y-%m-%d")}'
    raw_filename = f'{data_prefix[0]}_{filename}.json'
    clean_part_data_dir = f'{data_prefix[2]}_{filename}'

    bq_dataset_name = 'sf_eviction'
    bq_table_name_external = f'external_{filename_o}' 

    
    content = get_json(SODA_url, SODA_headers)
    raw_filepath = write_to_local(content, data_dir, raw_filename)
    write_to_gcs_subflow(raw_filepath)
    clean_datapath = clean_data(raw_filepath, data_dir, clean_part_data_dir)
    write_to_gcs_subflow(clean_datapath)
    write_to_bq(bq_dataset_name, bq_table_name_external, bq_table_name=filename_o, clean_datapath=clean_datapath)
    
    # testing
    # raw_filepath = 'data_eviction/2023/3/26/raw_eviction_2023-03-26.json'
    # clean_datapath = 'data_eviction/2023/3/26/clean_partitioned_eviction_2023-03-26' 



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