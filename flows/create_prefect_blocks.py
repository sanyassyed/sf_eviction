# creating prefect reusable blocks
from prefect_gcp import GcpCredentials, GcsBucket
from decouple import config, AutoConfig
from pathlib import Path

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


# https://docs.prefect.io/concepts/blocks/
# if a block has been created in a .py file, the block can also be registered with the CLI command:
# prefect block register --file flows/prefect_gcp_block.py