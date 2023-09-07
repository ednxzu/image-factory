# 🏭 image-factory

This repository houses the code for ednz-cloud openstack infrastructure, deployed with kolla-ansible.

## ⚙ requirements

### 📦 package requirements

In order to be able to test builds locally, you will need a few tools.

Install the dependencies.
```bash
ansible (to build packer files, as well as provision containers and AMIs)
packer (to build AMI and container images)
vault (to decrypt credentials/clouds.yaml)
```

### :lock: authenticate to vault

To be able to unencrypt sensitive files, and access passwords, you will need to authenticate to vault and retrieve a token that has read access to the `kv/image-factory` mount.

The following environment variables are required (or a .vault_token helper file)
```bash
export VAULT_ADDR=<vault api address>
export VAULT_TOKEN=<your vault token>
```

### 🛠 generate packer build files

In order to build images, you will need to generate the necessary packer files.

To do so, run:
```bash
BUILD_GROUP=<your-build-group> bash build.sh
```
Where `<your-build-group>` is the name of one of the inventory, without its extension (for example, `ansible-runners` will build the packer files for the `ansible-runners.yml` production inventory)

Note that `devel` inventories should not be built. They are mainly here to test out new layouts.

## 🏗 build images

### 🏡 local builds

Once the files have been generated, use the standard packer commands to build.
```bash
packer init packer/builds/<image_to_build>/<image_to_build>.pkr.hcl
packer validate packer/builds/<image_to_build>/<image_to_build>.pkr.hcl
packer build packer/builds/<image_to_build>/<image_to_build>.pkr.hcl
```

> **Warning**
> These commands should be run from the root of the repository, as all the paths are relative to it.
