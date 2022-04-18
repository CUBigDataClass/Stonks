terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
    }
  }
}

resource "google_compute_address" "static" {
  name = "ipv4-address"
  #name="34.106.21.144" 
  #name="static-address"
  #address_type= "EXTERNAL"
  #address="34.106.21.144"
  #region="us-west3"
}

resource "google_compute_network" "vpc_network" {
  name                    = "tf-network1"
  auto_create_subnetworks = "true"
}

resource "google_compute_firewall" "ssh-rule" {
  name = "demo-ssh2"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports = ["22","8000","80"]
  }
  target_tags = ["test1","http-server","https-server"]
  source_ranges = ["0.0.0.0/0"]
}

provider "google" {
//credentials needed as editor
  credentials = file("tfcreds.json")
  project = "my-project123-1470624985010"
  region  = "us-west3"
  zone    = "us-west3-a"
}

resource "google_compute_instance" "vm_instance" {
  name         = "test2"
  #too small. ran out of ram
  machine_type = "f1-micro"
  #machine_type = "e2-medium"

  tags=["ssh","http-server","test1"]

  boot_disk {
    initialize_params {
      image="ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }
  //public ssh key
  metadata = {
    ssh-keys = "jyoum741:${file("./my-ssh-key.pub")}"
  }

  network_interface {
    # A default network is created for all GCP projects
    network = google_compute_network.vpc_network.self_link
    access_config {
      #nat_ip = google_compute_address.static.address
 
    }
  }

  //private ssh key
  connection {
    type     = "ssh"
    user     = "jyoum741"
    host     = self.network_interface[0].access_config[0].nat_ip
    //host= google_compute_address.static.address
    private_key=file("my-ssh-key")
  }

  //destination has to be set to tmp because its the only writable directory
  provisioner "file"{
    source="django"
    destination="/tmp"
  }

  #download docker, download docker compose, build then execute
   provisioner "remote-exec"{
     inline=[
       "sudo mv /tmp/django /home/jyoum741",
       "curl -sSL https://get.docker.com/ | sudo sh",
      #  "docker run docker/compose:1.24.0 version",
      #  "sudo curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
      #  "sudo chmod +x /usr/local/bin/docker-compose",
     ]
  }
}
 

