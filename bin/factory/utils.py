import os
import yaml
from colorama import Fore, Style

ENV_VAR_IMAGE_FACTORY_ENV = "IMAGE_FACTORY_ENV"
ENV_VAR_IMAGE_FACTORY_INVENTORY = "IMAGE_FACTORY_INVENTORY"
ENV_VAR_IMAGE_FACTORY_VAULT_ADDR = "VAULT_ADDR"
ENV_VAR_IMAGE_FACTORY_VAULT_TOKEN = "VAULT_TOKEN"
ENV_VAR_IMAGE_FACTORY_VAULT_APPROLE_ID = "IMAGE_FACTORY_VAULT_APPROLE_ID"
ENV_VAR_IMAGE_FACTORY_VAULT_APPROLE_SECRET_ID = "IMAGE_FACTORY_VAULT_APPROLE_SECRET_ID"

default_config = {
    "inventory_path": "ansible/inventory",
    "build_path": "packer/builds",
    "generate_playbook_path": "ansible/generate.yml",
    "test_playbook_path": "ansible/test.yml",
}

logo_mapping = {
    "pass": f"{Fore.GREEN}✔{Style.RESET_ALL}",
    "fail": f"{Fore.RED}✘{Style.RESET_ALL}",
    "warning": f"{Fore.YELLOW}⚠{Style.RESET_ALL}",
    "deleted": f"{Fore.RED}🗑️{Style.RESET_ALL}",
}


def load_config():
    loaded_config = {}

    try:
        with open("factory.yml", "r") as config_file:
            loaded_config = yaml.safe_load(config_file) or {}
    except FileNotFoundError:
        pass  # Ignore if the file is not found

    # Merge the loaded config with the default config, giving precedence to loaded values
    config = {**default_config, **loaded_config}

    if "vault_addr" not in config:
        config["vault_addr"] = os.environ.get(ENV_VAR_IMAGE_FACTORY_VAULT_ADDR, None)
    if "vault_approle_id" not in config:
        config["vault_approle_id"] = os.environ.get(
            ENV_VAR_IMAGE_FACTORY_VAULT_APPROLE_ID, None
        )
    if "vault_approle_secret_id" not in config:
        config["vault_approle_secret_id"] = os.environ.get(
            ENV_VAR_IMAGE_FACTORY_VAULT_APPROLE_SECRET_ID, None
        )

    # Append values from environment variables
    config["image_factory_env"] = os.environ.get(ENV_VAR_IMAGE_FACTORY_ENV, None)
    config["image_factory_inventory"] = [
        inv
        for inv in os.environ.get(ENV_VAR_IMAGE_FACTORY_INVENTORY, "").split(",")
        if inv
    ]

    return config
