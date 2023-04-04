# Introduction:
Find here the sample contents of the ignored files which mainly consisted of the ones that were used to set the enviroment variables.

## **.env** file
```
# API
API_KEY_ID=xxxxxxxxxx
API_KEY_SECRET=xxxxxxxxxx
API_TOKEN =xxxxxxxxxx

###################################################################

# GCP
GCP_PROJECT_ID=xxxxxxxxxx
GCP_ZONE=xxxxxxxxxx
GCP_COMPUTE_ENGINE_NAME=xxxxxxxxxx
```

## **env.bashrc** file
```
# CREDENTIALS
###################################################################
# GCP
export GCP_PROJECT_ID=xxxxxxxxxx
export GCP_ZONE=xxxxxxxxxx
export GCP_COMPUTE_ENGINE_NAME=xxxxxxxxxx

```


.env file structure
# CREDENTIALS
###################################################################

# SODU API
API_KEY_ID=xxxxxxxxxx
API_KEY_SECRET=xxxxxxxxxx
API_TOKEN=xxxxxxxxxx

# GCP
GCP_PROJECT_ID=xxxxxxxxxx
GCP_ZONE=xxxxxxxxxx
GCP_COMPUTE_ENGINE_NAME=xxxxxxxxxx
# Get this info from the .json key
GCP_TYPE=xxxxxxxxxx
GCP_SERVICE_ACCOUNT_EMAIL=xxxxxxxxxx
GCP_KEY_ID=xxxxxxxxxx
GCP_PRIVATE_KEY=xxxxxxxxxx\n-----END PRIVATE KEY-----\n
GCP_CLIENT_ID=xxxxxxxxxx
GCP_AUTH_URI=xxxxxxxxxx
GCP_TOKEN_URI=xxxxxxxxxx
GCP_AUTH_PROVIDER=xxxxxxxxxx
GCP_CLIENT_CERT=xxxxxxxxxx
GCS_BUCKET=xxxxxxxxxx

# Prefect Credentials
PREFECT_CLOUD_API=xxxxxxxxxx
GCP_CREDENTIALS_BLOCK=xxxxxxxxxx
GCS_BUCKET_BLOCK=xxxxxxxxxx
BQ_BLOCK=xxxxxxxxxx

#dbt
DBT_PROJECT_DIRxxxxxxxxxx
BQ_DATASET_NAME_RAWxxxxxxxxxx
BQ_DATASET_NAME_DEVxxxxxxxxxx
BQ_DATASET_NAME_PRODxxxxxxxxxx
BQ_TABLE_NAME_RAW=xxxxxxxxxx
BQ_TABLE_NAME_STG=xxxxxxxxxx
BQ_TABLE_NAME_FACT=xxxxxxxxxx
