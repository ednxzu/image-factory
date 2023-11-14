import os
import subprocess
from factory.utils import load_config, logo_mapping
from .vault_utils import vault_login_approle, vault_logout_approle


def run_ansible_playbook(inventory, playbook_path, build_group=None, env=None):
    config = load_config()
    playbook_path = os.path.abspath(playbook_path)
    inventory_path = config.get("inventory_path")
    env = env or config.get("image_factory_env")
    inventory_file = f"{inventory_path}/{env}/{inventory}.yml"
    command = [
        "ansible-playbook",
        "-i",
        inventory_file,
        playbook_path,
        "-e",
        f"build_group={build_group}",
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return "fail"

    return "pass"


def print_status_message(action, inventory, build_group, env, status):
    logo = logo_mapping.get(status, "")
    print(
        f"{action} Ansible playbook for inventory '{inventory}' "
        f"with build_group '{build_group}' and environment '{env}': {logo}"
    )


def generate_packer_files(args):
    config = load_config()
    vault_accessor_id = None

    if args.vault_login:
        vault_accessor_id = vault_login_approle(
            vault_addr=config["vault_addr"],
            vault_approle_id=config["vault_approle_id"],
            vault_approle_secret_id=config["vault_approle_secret_id"],
        )

    env = args.env or config.get("image_factory_env")
    inventory = args.inventory
    build_group = args.build_group

    if not inventory:
        inventory = config.get("image_factory_inventory")

    generate_playbook_path = config.get("generate_playbook_path")

    if inventory:
        for inv in inventory:
            status = run_ansible_playbook(
                inv,
                playbook_path=generate_playbook_path,
                build_group=build_group,
                env=env,
            )
            print_status_message("Running", inv, build_group, env, status)

    else:
        print(
            "Error: no inventory specified. "
            "You need to set the --inventory/-i flag, or set IMAGE_FACTORY_INVENTORY."
        )

    if vault_accessor_id:
        vault_logout_approle(
            vault_addr=config["vault_addr"], vault_token_accessor_id=vault_accessor_id
        )


def test_inventory(args):
    config = load_config()
    vault_accessor_id = None

    if args.vault_login:
        vault_accessor_id = vault_login_approle(
            vault_addr=config["vault_addr"],
            vault_approle_id=config["vault_approle_id"],
            vault_approle_secret_id=config["vault_approle_secret_id"],
        )

    env = args.env
    inventory = args.inventory
    build_group = args.build_group

    if not inventory:
        inventory = config.get("image_factory_inventory", [])

    test_playbook_path = config.get("test_playbook_path")

    if inventory:
        for inv in inventory:
            status = run_ansible_playbook(
                inv,
                playbook_path=test_playbook_path,
                build_group=build_group,
                env=env,
            )
            print_status_message("Running", inv, build_group, env, status)

    else:
        print(
            "Error: no inventory specified. "
            "You need to set the --inventory/-i flag, or set IMAGE_FACTORY_INVENTORY."
        )

    if vault_accessor_id:
        vault_logout_approle(
            vault_addr=config["vault_addr"], vault_token_accessor_id=vault_accessor_id
        )
