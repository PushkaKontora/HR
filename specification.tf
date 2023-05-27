terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

provider "yandex" {
  token     = local.token
  cloud_id  = local.cloud_id
  folder_id = local.folder_id
  zone      = local.zone
}

locals {
  token       =
  cloud_id    =
  folder_id   =
  zone        =
  image_id    =
  db_user     =
  db_password =
}

resource "yandex_container_registry" "this" {
  name      = "hr-registry"
  folder_id = local.folder_id
}

resource "null_resource" "push_app" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "docker build backend/ -t cr.yandex/${yandex_container_registry.this.id}/app --push"
  }
}

resource "null_resource" "push_nginx" {
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "docker build frontend/hr-portal/ -t cr.yandex/${yandex_container_registry.this.id}/nginx --push"
  }
}

resource "yandex_iam_service_account" "sa" {
  name = "hr-storage"
}

resource "yandex_resourcemanager_folder_iam_member" "sa_editor" {
  folder_id = local.folder_id
  role      = "editor"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = yandex_iam_service_account.sa.id
}

resource "yandex_storage_bucket" "this" {
  access_key = yandex_iam_service_account_static_access_key.sa-static-key.access_key
  secret_key = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
  bucket     = "hr-portal-peroovy"
}

data "template_file" "app_init" {
  template = file("app-init.yaml")
  vars = {
    YC_TOKEN                = local.token
    REGISTRY_ID             = yandex_container_registry.this.id
    POSTGRES_DB             = yandex_mdb_postgresql_database.hr.name
    POSTGRES_USER           = yandex_mdb_postgresql_user.peroovy.name
    POSTGRES_PASSWORD       = yandex_mdb_postgresql_user.peroovy.password
    POSTGRES_HOST           = yandex_mdb_postgresql_cluster.this.host[0].fqdn
    POSTGRES_PORT           = 6432
    AWS_ACCESS_KEY_ID       = yandex_storage_bucket.this.access_key
    AWS_SECRET_ACCESS_KEY   = yandex_storage_bucket.this.secret_key
    AWS_STORAGE_BUCKET_NAME = yandex_storage_bucket.this.bucket
    AWS_S3_ENDPOINT_URL     = "https://storage.yandexcloud.net"
  }
}

data "template_file" "nginx_init" {
  template = file("nginx-init.yaml")
  vars = {
    SSH_KEY     = file("~/.ssh/id_rsa.pub")
    YC_TOKEN    = local.token
    REGISTRY_ID = yandex_container_registry.this.id
    APP_HOST    = yandex_compute_instance.app.network_interface.0.ip_address
  }
}

resource "yandex_compute_instance" "app" {
  name        = "app"
  zone        = local.zone
  platform_id = "standard-v1"

  resources {
    cores  = 2
    memory = 4
  }

  boot_disk {
    initialize_params {
      image_id = local.image_id
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet_a.id
  }

  metadata = {
    user-data          = data.template_file.app_init.rendered
    serial-port-enable = 1
  }

  depends_on = [null_resource.push_app]
}

resource "yandex_compute_instance" "nginx" {
  name        = "nginx"
  zone        = local.zone
  platform_id = "standard-v1"

  resources {
    cores  = 2
    memory = 4
  }

  boot_disk {
    initialize_params {
      image_id = local.image_id
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet_a.id
    nat       = true
  }

  metadata = {
    user-data          = data.template_file.nginx_init.rendered
    serial-port-enable = 1
  }

  depends_on = [null_resource.push_nginx]
}

resource "yandex_mdb_postgresql_cluster" "this" {
  name        = "hr"
  environment = "PRESTABLE"
  network_id  = yandex_vpc_network.this.id

  config {
    version = 14
    resources {
      resource_preset_id = "c3-c2-m4"
      disk_type_id       = "network-hdd"
      disk_size          = 10
    }
  }

  host {
    zone      = local.zone
    subnet_id = yandex_vpc_subnet.subnet_a.id
  }
}

resource "yandex_mdb_postgresql_database" "hr" {
  cluster_id = yandex_mdb_postgresql_cluster.this.id
  name       = "hr"
  owner      = yandex_mdb_postgresql_user.peroovy.name
}

resource "yandex_mdb_postgresql_user" "peroovy" {
  cluster_id = yandex_mdb_postgresql_cluster.this.id
  name       = local.db_user
  password   = local.db_password
}

resource "yandex_vpc_network" "this" {
  name = "hr-network"
}

resource "yandex_vpc_subnet" "subnet_a" {
  name           = "subnet-a"
  zone           = local.zone
  network_id     = yandex_vpc_network.this.id
  v4_cidr_blocks = ["10.2.0.0/16"]
  route_table_id = yandex_vpc_route_table.this.id
}

resource "yandex_vpc_gateway" "nat_gateway" {
  shared_egress_gateway {}
}

resource "yandex_vpc_route_table" "this" {
  network_id = yandex_vpc_network.this.id

  static_route {
    destination_prefix = "0.0.0.0/0"
    gateway_id         = yandex_vpc_gateway.nat_gateway.id
  }
}