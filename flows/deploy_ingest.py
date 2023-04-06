from prefect.deployments import Deployment
from ingest import etl_parent_flow
from prefect.orion.schemas.schedules import CronSchedule
from decouple import config, AutoConfig
config = AutoConfig(search_path='.env')

filename_o = config("DBT_ENV_BQ_TABLE_RAW")
dataset_name = config("DATASET_NAME")
target_dbt = 'prod'

# Deployment for Loading data to GCS from the web
local_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='etl_web_to_gcp', work_queue_name="development", entrypoint="flows/ingest.py:etl_parent_flow", schedule =(CronSchedule(cron="5 0 1 * *", timezone="America/Chicago")), parameters={"dataset_name":dataset_name, "filename_o":filename_o, "target_dbt":target_dbt})


if __name__=="__main__":
    """Builds the Deployment and Applies the Deployment by parameterizing the flow"""
    local_dep.apply()

# Optional CLI
# Build & Schedule & Apply in 1 step
# `prefect deployment build ingest.py:etl_parent_flow -n "web_to_gcp_etl" --cron "5 0 1 * ?" --timezone "UTC" -a`

# Run this script & and deploy the flow on Prefect Cloud(make sure you are logged into prefect cloud)
# python flows/deploy_ingest.py
# Check the UI if deployment is available
# Start the prefect agent in detaches mode
# screen -A -m -d -S prefectagent prefect agent start --work-queue "development"
# Force run the deployment
# prefect deployment run ParentFlow/etl_web_to_gcp