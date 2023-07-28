packer {
  required_plugins {
    docker = {
      version = "~> 1"
      source  = "github.com/hashicorp/docker"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = "~> 1"
    }
  }
}

source "docker" "standard_docker_node_18" {
  image  = "node:18-bookworm"
  commit = true
  login = false
  run_command = ["-d", "-i", "-t", "--name", "standard_docker_node_18", "{{.Image}}", "/bin/bash"]
}

build {
  name = "learn-packer"
  sources = [
    "source.docker.standard_docker_node_18"
  ]
  provisioner "shell" {
    environment_vars = [
      "FOO=hello world",
    ]
    inline = [
      "echo Adding file to Docker Container",
      "echo \"FOO is $FOO\" > example.txt",
    ]
  }

  provisioner "ansible" {
    ansible_env_vars = ["ANSIBLE_HOST_KEY_CHECKING=false"]
    extra_arguments  = ["-e ansible_connection=docker", "-e ansible_python_interpreter=/usr/bin/python3", "-e ansible_host=standard_docker_node_18", "-e builder_type=docker", "-e target_host=standard_docker_node_18"]
    inventory_file   = "../../ansible/inventory/production/standard-runners.yml"
    playbook_file    = "../../ansible/01_test.yml"
    user             = "root"
  }
}
