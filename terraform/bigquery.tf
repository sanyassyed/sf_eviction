# DWH
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset_raw" {
  dataset_id = var.DATASET_RAW
  project    = var.PROJECT_ID
  location   = var.REGION
}
resource "google_bigquery_dataset" "dataset_dev" {
  dataset_id = var.DATASET_DEV
  project    = var.PROJECT_ID
  location   = var.REGION
}

resource "google_bigquery_dataset" "dataset_prod" {
  dataset_id = var.DATASET_PROD
  project    = var.PROJECT_ID
  location   = var.REGION
}