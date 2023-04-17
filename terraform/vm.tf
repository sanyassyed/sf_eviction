resource "google_compute_instance" "agent-vm" {
  name         = var.COMPUTE_ENGINE_NAME
  machine_type = var.COMPUTE_ENGINE_MACHINE_TYPE
  zone         = var.COMPUTE_ENGINE_ZONE

  boot_disk {
    initialize_params {
      image = var.COMPUTE_ENGINE_MACHINE_IMAGE
      size=40
    }
  }

  service_account {
    email = "${var.SERVICE_ACCOUNT_NAME}@${var.PROJECT_ID}.iam.gserviceaccount.com"
    scopes = [
      "cloud-platform",
    ]
  }

  metadata {
    sshKeys = "${var.SSH_USER}:${file(var.SSH_PUB_KEY_FILE)}"
  }

  network_interface {
    network = "default"
    access_config {
        network_tier = "PREMIUM"
    }
  }

  scheduling {
    on_host_maintenance="MIGRATE"
  }

}