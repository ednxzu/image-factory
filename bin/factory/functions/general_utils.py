import os
from tabulate import tabulate
from factory.utils import load_config, logo_mapping

def is_in_env_var(inventory, defined_in_env):
    if inventory in defined_in_env:
        return "pass"
    else:
        return "fail"

def list_inventories(args):
    config = load_config()
    env = args.env
    inventory_dir = os.path.join(config.get("inventory_path", ""), env)  # Update this with the actual path

    if not os.path.exists(inventory_dir):
        print(f"Error: Directory '{inventory_dir}' not found.")
        return

    files = [f for f in os.listdir(inventory_dir) if f.endswith(".yml")]

    if not files:
        print(f"No inventory files found in '{inventory_dir}'.")
        return

    defined_in_env = os.environ.get("IMAGE_FACTORY_INVENTORY", "").split(',')

    table_data = [("Inventory Name", "Automatic build")]
    for f in files:
        inventory_name = f[:-4]  # Remove the '.yml' extension
        status = is_in_env_var(inventory_name, defined_in_env)
        logo = logo_mapping.get(status, "")
        table_data.append((inventory_name, logo))

    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))



def create_inventory(inventory_directory, environment, inventory_name):
    return


def delete_inventory(inventory_directory, environment, inventory_name):
    return
