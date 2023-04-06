# creating prefect reusable blocks
from prefect_gcp import GcpCredentials, GcsBucket, BigQueryWarehouse
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile, DbtCoreOperation
from decouple import config, AutoConfig
from pathlib import Path
import os

config = AutoConfig(search_path='.env')
##################################################################################
# GCP CREDENTIALS BLOCK

# https://github.com/discdiver/prefect-zoomcamp/blob/main/blocks/make_gcp_blocks.py
# Run only when setting the blocks for reuse later
# credentials from json file
# we use this rather than passing a json file 
GCP_TYPE=config("GCP_TYPE")
GCP_PROJECT_ID = config("GCP_PROJECT_ID") 
GCP_KEY_ID=config("GCP_KEY_ID")
GCP_PRIVATE_KEY=config("GCP_PRIVATE_KEY")
GCP_SERVICE_ACCOUNT_EMAIL=config("GCP_SERVICE_ACCOUNT_EMAIL")
GCP_CLIENT_ID=config("GCP_CLIENT_ID")
GCP_AUTH_URI=config("GCP_AUTH_URI")
GCP_TOKEN_URI=config("GCP_TOKEN_URI")
GCP_AUTH_PROVIDER=config("GCP_AUTH_PROVIDER")
GCP_CLIENT_CERT=config("GCP_CLIENT_CERT")

GCP_CREDENTIALS_BLOCK=config("GCP_CREDENTIALS_BLOCK")
# The advantage of using service_account_info, instead of service_account_file, is that it is accessible across containers.
# replace this PLACEHOLDER dict with your own service account info
# https://prefecthq.github.io/prefect-gcp/


# Option 1
# service_account_file = Path("/home/sanyashireen/.google/credentials/google_credentials.json")
#GcpCredentials(service_account_file=service_account_file).save("gcp_credentials_eviction")

# Option 2
service_account_info_dict = {
  "type":GCP_TYPE,
  "project_id":GCP_PROJECT_ID,
  "private_key_id":GCP_KEY_ID,
  "private_key":GCP_PRIVATE_KEY.replace('\\n', '\n'), # to handle the new line which was being replaced by \n by python
  "client_email":GCP_SERVICE_ACCOUNT_EMAIL,
  "client_id":GCP_CLIENT_ID,
  "auth_uri":GCP_AUTH_URI,
  "token_uri":GCP_TOKEN_URI,
  "auth_provider_x509_cert_url":GCP_AUTH_PROVIDER,
  "client_x509_cert_url":GCP_CLIENT_CERT
}
GcpCredentials(service_account_info=service_account_info_dict).save(GCP_CREDENTIALS_BLOCK, overwrite=True)


#########################################################################################################
# GCS BUCKET BLOCK

gcp_credentials = GcpCredentials.load(GCP_CREDENTIALS_BLOCK)

# Creating GCS Bucket Block
gcs_bucket=config("GCS_BUCKET")
gcs_bucket_block =config("GCS_BUCKET_BLOCK")

GcsBucket(gcp_credentials=gcp_credentials,bucket=gcs_bucket).save(gcs_bucket_block, overwrite=True)



#########################################################################################################
# BQ BUCKET BLOCK

gcp_credentials = GcpCredentials.load(GCP_CREDENTIALS_BLOCK)

# Creating BQ Bucket Block
bq_block =config("BQ_BLOCK")

BigQueryWarehouse(gcp_credentials=gcp_credentials).save(bq_block, overwrite=True)

#########################################################################################################
# DBT CORE CLI BLOCKS
bq_dataset_dev = config("DBT_ENV_BQ_DS_DEV")
bq_dataset_prod = config("DBT_ENV_BQ_DS_PROD")
dbt_target_dev_block= config("DBT_CLI_TARGET_DEV_BLOCK")
dbt_target_prod_block= config("DBT_CLI_TARGET_PROD_BLOCK")
dbt_profile_dev_block= config("DBT_CLI_PROFILE_DEV_BLOCK")
dbt_profile_prod_block= config("DBT_CLI_PROFILE_PROD_BLOCK")
dbt_dir =config("DBT_ENV_PROJECT_DIR")
dbt_dir_path = f"{os.getcwd()}/{dbt_dir}"

# DEVELOPMENT BLOCKS
# 1.TARGET 
target_configs_dev = BigQueryTargetConfigs(
    schema=bq_dataset_dev,  # also known as dataset
    credentials=gcp_credentials,
)
target_configs_dev.save(dbt_target_dev_block, overwrite=True)

# 2.PROFILE
dbt_cli_profile_dev = DbtCliProfile(
    name="sf_eviction_dbt", # find this in the profiles.yml or under name in dbt_project.yml
    target="dev",
    target_configs=target_configs_dev,
)
dbt_cli_profile_dev.save(dbt_profile_dev_block, overwrite=True)

# 3.OPERATION / COMMANDS
#dbt_cli_profile_dev_block = config("DBT_CLI_PROFILE_DEV_BLOCK")
dbt_cli_command_dev_block = config("DBT_CLI_COMMAND_DEV_BLOCK") 

#dbt_cli_profile_dev = DbtCliProfile.load(dbt_cli_profile_dev_block)
dbt_core_operation_dev = DbtCoreOperation(
    commands=["dbt build --var 'is_test_run: false'"],
    dbt_cli_profile=dbt_cli_profile_dev,
    working_dir=dbt_dir_path,
    project_dir=dbt_dir_path,
    overwrite_profiles=True,
)
dbt_core_operation_dev.save(dbt_cli_command_dev_block, overwrite=True)


# DEVELOPMENT BLOCKS
# 1.TARGET 
target_configs_prod = BigQueryTargetConfigs(
    schema=bq_dataset_prod,  # also known as dataset
    credentials=gcp_credentials,
)
target_configs_prod.save(dbt_target_prod_block, overwrite=True)

# 2.PROFILE
dbt_cli_profile_prod = DbtCliProfile(
    name="sf_eviction_dbt", # find this in the profiles.yml or under name in dbt_project.yml
    target="prod",
    target_configs=target_configs_prod,
)
dbt_cli_profile_prod.save(dbt_profile_prod_block, overwrite=True)

# 3.OPERATION / COMMANDS
dbt_cli_command_prod_block = config("DBT_CLI_COMMAND_PROD_BLOCK") 

dbt_core_operation_prod = DbtCoreOperation(
    commands=["dbt build --var 'is_test_run: false'"],
    dbt_cli_profile=dbt_cli_profile_prod,
    working_dir=dbt_dir_path,
    project_dir=dbt_dir_path,
    overwrite_profiles=True,
)
dbt_core_operation_prod.save(dbt_cli_command_prod_block, overwrite=True)


# https://docs.prefect.io/concepts/blocks/
# if a block has been created in a .py file, the block can also be registered with the CLI command:
# NOTE: Log into prefect cloud before running the below command
# prefect block register --file flows/create_prefect_blocks.py
# Then log into prefect cloud and check that the blocks are availble in the UI