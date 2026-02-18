data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}


resource "yandex_compute_instance" "lendy" {
  count = 2

  name = "lendy-${count.index + 1}"
  hostname = "lendy-${count.index + 1}"

  resources {
    memory        = 2
    cores         = 2
  }

  boot_disk {
    initialize_params {
      name       = "disk-lendy-${count.index + 1}"
      type       = "network-ssd"
      size       = 10
      block_size = 4096
      image_id   = data.yandex_compute_image.ubuntu.id
    }
    auto_delete = true
  }

  # folder_id = "b1gdfsq84al32hk568ka"


  network_interface {
    subnet_id = "e2l7q23d0jq5as51sesr"
    nat       = true  
  }


  metadata = {
    user-data = file("${path.module}/users.yaml")
    # ssh-keys = <<-EOT
    # qwerty:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGLEaYmNInYEjTvkTzqVfisvIur5FeT5zM2a2szHNPvS lendy@fedora
    # EOT
  }

  scheduling_policy {
    preemptible = true
  }

  platform_id = "standard-v3"
  zone = "ru-central1-b"
}



#any steps for create vm, doesn't matter right now

# # 4. Security Group (SSH)
# resource "yandex_vpc_security_group" "ssh" {
#   name = "lendy-ssh"

#   egress {
#     protocol       = "ANY"
#     description    = "any"
#     from_port      = 0
#     to_port        = 65535
#     v4_cidr_blocks = ["0.0.0.0/0"]
#   }

#   ingress {
#     protocol       = "TCP"
#     description    = "SSH"
#     from_port      = 22
#     to_port        = 22
#     v4_cidr_blocks = ["0.0.0.0/0"] 
#   }
# }

# # 5. Outputs
# output "vm_ips" {
#   value = [for vm in yandex_compute_instance.lendy : 
#     "${vm.network_interface[0].nat_ip_address} (lendy-${vm.name})"
#   ]
# }



# resource "yandex_compute_disk" "boot-disk-1" {
#   count = 2
#   name       = "disk-ubuntu-lendy"
#   type       = "network-hdd"
#   zone       = "ru-central1-d"
#   size       = 10
#   image_id   = 
# }

# created network and subnet
# resource "yandex_vpc_network" "network" {
#   name = "lendy-network"
# }

# resource "yandex_vpc_subnet" "subnet" {
#   name           = "lendy-subnet"
#   zone           = "ru-central1-b"
#   network_id     = yandex_vpc_network.network.id
#   v4_cidr_blocks = ["192.168.10.0/24"]
# }