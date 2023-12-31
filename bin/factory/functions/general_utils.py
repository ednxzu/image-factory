import os
from tabulate import tabulate
import json
from factory.utils import load_config, logo_mapping


def is_in_env_var(inventory, defined_in_env):
    return "pass" if inventory in defined_in_env else "fail"

def list_inventories(args):
    config = load_config()
    env = args.env

    if not env:
        print(
            "Error: Please provide the environment with the --env flag or set the IMAGE_FACTORY_ENV environment variable."
        )
        return

    inventory_dir = os.path.join(config.get("inventory_path"), env)

    if not os.path.exists(inventory_dir):
        print(f"Error: Directory '{inventory_dir}' not found.")
        return

    defined_in_env = config.get("image_factory_inventory")

    files = [f[:-4] for f in os.listdir(inventory_dir) if f.endswith(".yml")]

    if not files:
        print(f"No inventory files found in '{inventory_dir}'.")
        return

    if args.json:
        print(json.dumps(files))
    else:
        # Display in tabular format
        table_headers = ["Inventory Name", "Automatic build"]
        table_data = [table_headers]

        for inventory_name in files:
            status = is_in_env_var(inventory_name, defined_in_env)
            logo = logo_mapping.get(status, "")
            table_data.append((inventory_name, logo))


        print(tabulate(table_data, headers="firstrow", tablefmt="grid"))



def create_inventory(inventory_directory, environment, inventory_name):
    return


def delete_inventory(inventory_directory, environment, inventory_name):
    return
