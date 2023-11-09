import os
import tabulate


def list_inventories(inventory_directory, environment):
    try:
        env_dir = environment
        files = [
            file
            for file in os.listdir(f"{inventory_directory}/{env_dir}")
            if os.path.isfile(os.path.join(inventory_directory, env_dir, file))
        ]
        table = [["Inventory Files"]]
        table.extend([[file] for file in files])
        print(tabulate.tabulate(table, headers="firstrow", tablefmt="grid"))
    except FileNotFoundError:
        print("Inventory directory not found.")
        return


def create_inventory(inventory_directory, environment, inventory_name):
    return


def delete_inventory(inventory_directory, environment, inventory_name):
    return
