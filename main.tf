
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

resource "google_compute_network" "vpc_network" {
  name                    = "tf-network"
  auto_create_subnetworks = "true"
}

resource "google_compute_firewall" "ssh-rule" {
  name = "demo-ssh"
  network = google_compute_network.vpc_network.name
  allow {
    protocol = "tcp"
    ports = ["22"]
  }
  target_tags = ["test1"]
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
  name         = "testrun"
  #too small. ran out of ram
  #machine_type = "f1-micro"
  machine_type = "e2-medium"

  tags=["ssh","http-server","test1"]

  boot_disk {
    initialize_params {
      #this fkn image has no exec flag
      #image = "cos-cloud/cos-85-13310-1416-13"
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
    source="tcompose"
    destination="/tmp"
  }

  //download docker, download docker compose, build then execute
  provisioner "remote-exec"{
    inline=[
      "sudo mv /tmp/tcompose /home/jyoum741",
      "curl -sSL https://get.docker.com/ | sudo sh",
      "docker run docker/compose:1.24.0 version",
      "sudo curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose",
      "cd /home/jyoum741/tcompose",
      "sudo docker-compose build",
      "sudo docker-compose up",
    ]
  }
}
 

