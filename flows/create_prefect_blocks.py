# creating prefect reusable blocks
from prefect_gcp import GcpCredentials, GcsBucket, BigQueryWarehouse
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile, DbtCoreOperation
from decouple import config, AutoConfig
from pathlib import Path
import os

config = AutoConfig(search_path='.env')
##################################################################################
# GCP CREDENTIALS BLOCK

##################################################################################
# GCP CREDENTIALS BLOCK

GCP_CREDENTIALS_BLOCK=config("GCP_CREDENTIALS_BLOCK")

service_account_file = Path("credentials/gcp-credentials.json")
GcpCredentials(service_account_file=service_account_file).save(GCP_CREDENTIALS_BLOCK, overwrite=True)


#########################################################################################################
# GCS BUCKET BLOCK

gcp_credentials = GcpCredentials.load(GCP_CREDENTIALS_BLOCK)

# Creating GCS Bucket Block
gcs_bucket=config("GCS_BUCKET_NAME")
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
    commands=["dbt deps", "dbt build --var 'is_test_run: false'"],
    dbt_cli_profile=dbt_cli_profile_dev,
    working_dir=dbt_dir_path,
    project_dir=dbt_dir_path,
    overwrite_profiles=True,
)
dbt_core_operation_dev.save(dbt_cli_command_dev_block, overwrite=True)


# PRODUCTION BLOCKS
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