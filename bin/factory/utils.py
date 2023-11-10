import os
import yaml
from colorama import Fore, Style


default_config = {
    "inventory_path": "ansible/inventory",
    "generate_playbook_path": "ansible/01_generate_templates.yml",
    "test_playbook_path": "ansible/02_test.yml"
}

logo_mapping = {
    "pass": f"{Fore.GREEN}✔{Style.RESET_ALL}",
    "fail": f"{Fore.RED}❌{Style.RESET_ALL}",
    "warning": f"{Fore.YELLOW}⚠{Style.RESET_ALL}",
    "deleted": f"{Fore.RED}🗑️{Style.RESET_ALL}"
}

def load_config():
    try:
        with open("factory.yml", "r") as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        config = default_config
    return config
