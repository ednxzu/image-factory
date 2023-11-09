import os
import yaml


default_config = {
    "inventory_path": "ansible/inventory",
}


def load_config():
    try:
        with open("factory.yml", "r") as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        config = default_config
    return config
