terraform {
  required_version = ">= 1.0"
  backend "local" {}  # Can change from "local" to "gcs" (for google) or "s3" (for aws), if you would like to preserve your tf-state online
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.PROJECT_ID
  region = var.REGION
  credentials = file(var.SERVICE_ACCOUNT_CREDENTIAL_PATH)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

