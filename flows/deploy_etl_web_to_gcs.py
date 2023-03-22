from prefect.deployments import Deployment
from etl_web_to_gcs import etl_parent_flow
from prefect.orion.schemas.schedules import CronSchedule

# Deployment for Loading data to GCS from the web
local_dep = Deployment.build_from_flow(flow = etl_parent_flow, name='web_to_gcs_etl', work_queue_name="development", entrypoint="flows/etl_web_to_gcs.py:etl_parent_flow", schedule =(CronSchedule(cron="5 0 1 * *", timezone="America/Chicago")), parameters={"dataset_name":'5cei-gny5', "filename":"eviction"})


if __name__=="__main__":
    """Builds the Deployment and Applies the Deployment by parameterizing the flow"""
    local_dep.apply()

# Optional CLI
# Build & Schedule & Apply in 1 step
# `prefect deployment build etl_web_to_gcs.py:etl_parent_flow -n "WebToGCS ETL" --cron "5 0 1 * ?" --timezone "UTC" -a`

# Run this script
# python flows/deplot_etl_web_gcs.py