import os
import argparse
from .functions.general_utils import (
    list_inventories,
    create_inventory,
    delete_inventory,
)
from .functions.ansible_utils import generate_packer_files, test_inventory
from .functions.vault_utils import vault_login_approle
from .utils import ENV_VAR_IMAGE_FACTORY_ENV, ENV_VAR_IMAGE_FACTORY_INVENTORY


def set_default_string_from_env(parser: argparse.ArgumentParser, env_var: str):
    if env_var in os.environ:
        parser.set_defaults(env=os.environ[env_var])


def set_default_list_from_env(parser: argparse.ArgumentParser, env_var: str):
    if env_var in os.environ:
        parser.set_defaults(
            env=[inv for inv in os.environ.get(env_var, "").split(",") if inv]
        )


def create_parser():
    parser = argparse.ArgumentParser(
        prog="factory",
        description="CLI tool to ease interactions with the image factory",
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="action")

    # "inventory" subparser
    inventory_parser = subparsers.add_parser(
        name="inventory", help="Interact with inventory objects"
    )
    inventory_subparsers = inventory_parser.add_subparsers(
        title="subcommands", dest="inventory_action"
    )

    # "inventory list" subcommand
    list_parser = inventory_subparsers.add_parser(
        name="list", help="List all inventories currently in the factory"
    )
    list_parser.set_defaults(func=list_inventories)
    list_parser.add_argument(
        "--env",
        "-e",
        required=False,
        help="The environment to list the inventories from.",
    )
    set_default_string_from_env(list_parser, ENV_VAR_IMAGE_FACTORY_ENV)

    # "inventory test" subcommand
    test_parser = inventory_subparsers.add_parser(
        name="test", help="Test inventory files."
    )
    test_parser.set_defaults(func=test_inventory)

    test_parser.add_argument(
        "--env",
        "-e",
        required=False,
        help="The environment where the inventory is located",
    )
    set_default_string_from_env(test_parser, ENV_VAR_IMAGE_FACTORY_ENV)

    test_parser.add_argument(
        "--inventory",
        "-i",
        required=False,
        nargs="+",
        help="The inventory to generate files from",
    )
    set_default_list_from_env(test_parser, ENV_VAR_IMAGE_FACTORY_INVENTORY)

    test_parser.add_argument(
        "--build-group",
        "-g",
        default="all",
        required=False,
        type=str,
        help="Specify a specific group to target within the inventory file",
    )

    test_parser.add_argument(
        "--vault-login",
        "-v",
        help="Login to vault prior to running the ansible playbook",
        action="store_true",
    )

    # "inventory create" subcommand
    create_parser = inventory_subparsers.add_parser(
        "create", help="Create a new inventory"
    )
    create_parser.add_argument("name", help="Name of the inventory to create")

    # "inventory delete" subcommand
    delete_parser = inventory_subparsers.add_parser(
        "delete", help="Delete an inventory"
    )
    delete_parser.add_argument("name", help="Name of the inventory to delete")

    # "generate" subparser
    generate_parser = subparsers.add_parser(
        name="generate", help="Generate packer files from a given inventory"
    )
    generate_parser.set_defaults(func=generate_packer_files)

    generate_parser.add_argument(
        "--env",
        "-e",
        required=True,
        help="The environment where the inventory is located",
    )
    set_default_string_from_env(generate_parser, ENV_VAR_IMAGE_FACTORY_ENV)

    generate_parser.add_argument(
        "--inventory",
        "-i",
        required=False,
        nargs="+",
        help="The inventory to generate files from",
    )
    set_default_list_from_env(generate_parser, ENV_VAR_IMAGE_FACTORY_INVENTORY)

    generate_parser.add_argument(
        "--build-group",
        "-g",
        default="all",
        required=False,
        type=str,
        help="Specify a specific group to target within the inventory file",
    )

    generate_parser.add_argument(
        "--vault-login",
        "-v",
        help="Login to vault prior to running the ansible playbook",
        action="store_true",
    )

    return parser
