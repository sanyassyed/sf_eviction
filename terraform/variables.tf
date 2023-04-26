# passed in by env vars (TF_VAR)
variable "PROJECT_ID" {}
variable "REGION" {}
variable "SERVICE_ACCOUNT_NAME" {}
variable "BUCKET_NAME" {}
variable "DATASET_RAW" {}
variable "DATASET_DEV" {}
variable "DATASET_PROD" {}
variable "COMPUTE_ENGINE_NAME" {}
variable "COMPUTE_ENGINE_MACHINE_TYPE" {}
variable "COMPUTE_ENGINE_MACHINE_IMAGE" {}
variable "COMPUTE_ENGINE_ZONE" {}
variable "SSH_USER" {}
variable "SSH_PUB_KEY_FILE" {}
variable "SERVICE_ACCOUNT_CREDENTIAL_PATH" {}
variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}




