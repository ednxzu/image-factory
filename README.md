# 🏭 image-factory

This repository houses the code for ednz-cloud openstack infrastructure, deployed with kolla-ansible.

## :gear: requirements

### :snake: python virtual environment

In order to get a functional kolla-ansible install, it is highly recommended to get a python virtual environment.

Install the dependencies.
```bash
sudo apt install git python3-dev libffi-dev gcc libssl-dev python3-venv
```

Create your virtual environment.
```bash
python3 -m venv /path/to/venv
source /path/to/venv/bin/activate
```

Install the requirements.
```bash
pip install -U pip
pip install 'ansible>=6,<8'
```

Install kolla-ansible.
```bash
pip install git+https://opendev.org/openstack/kolla-ansible@stable/2023.1
```

### :lock: authenticate to vault

To be able to unencrypt sensitive files, and access passwords, you will need to authenticate to vault and retrieve a token that has read access to the `kv_os/` mount.

The following environment variables are required (or a .vault_token helper file)
```bash
export VAULT_ADDR=<vault api address>
export VAULT_TOKEN=<your vault token>
```

### :key: get your passwords.yml file
To be able to work with this deployment, you'll need to populate your passwords.yml file.

Copy the `passwords.yml.sample` file from the repository.
```bash
cp etc/kolla/passwords.yml.sample <path/to/passwords.yml>
```

```bash
  kolla-readpwd -p <path/to/passwords.yml> \
  --vault-addr $VAULT_ADDR \
  --vault-token  $VAULT_TOKEN \
  --vault-mount-point kv_os \
  --vault-kv-path kolla/passwords
```

## :smiling_imp: the real deal

### :koala: run deployments against the production environment
To run deployments (or any other action) against the production environment, you can run the following command from the root of the git project.
```bash
  kolla-ansible --inventory inventory/production/hosts.ini \
  --configdir $(pwd)/etc/kolla \
  --passwords <path/to/passwords.yml> \
   <your-action> \
  --tags <your-tags-if-needed>
```