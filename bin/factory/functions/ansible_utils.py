import os
from factory.utils import load_config, logo_mapping


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
        os.system(" ".join(command))
    except Exception as e:
        print(f"Error running Ansible playbook: {e}")
        return "fail"

    return "pass"


def generate_packer_files(args):
    config = load_config()
    env = args.env or config.get("image_factory_env", "")
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
            logo = logo_mapping.get(status, "")
            print(
                f"Running Ansible generate playbook for inventory '{inv}' with build_group '{build_group}' and environment '{env}': {logo}"
            )

    else:
        print(
            "Error: no inventory specified. You need to set the --inventory/-i flag, or set IMAGE_FACTORY_INVENTORY."
        )


def test_inventory(args):
    config = load_config()
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
            logo = logo_mapping.get(status, "")
            print(
                f"Running Ansible test playbook for inventory '{inv}' with build_group '{build_group}' and environment '{env}': {logo}"
            )

    else:
        print(
            "Error: no inventory specified. You need to set the --inventory/-i flag, or set IMAGE_FACTORY_INVENTORY."
        )
