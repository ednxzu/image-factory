packer {
  required_plugins {
    docker = {
      version = "1.0.8"
      source  = "github.com/hashicorp/docker"
    }
  }
}

source "docker" "node18" {
  image  = "node:18-bookworm"
  commit = true
}

build {
  name = "learn-packer"
  sources = [
    "source.docker.node18"
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
}
