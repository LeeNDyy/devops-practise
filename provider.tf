terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
      version = "0.186.0"
    }
  }
  # required_version = "0.186"
}

provider "yandex" {
  token     = var.token
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = "ru-central1-b"
}

