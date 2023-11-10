import argparse
from .functions.general_utils import list_inventories, create_inventory, delete_inventory
from .functions.ansible_utils import generate_packer_files, test_inventory


def create_parser():
    parser = argparse.ArgumentParser(
        prog="factory", description="CLI tool to ease interactions with the image factory"
    )
    subparsers = parser.add_subparsers(title="subcommands", dest="action")

    # "inventory" subparser
    inventory_parser = subparsers.add_parser(
        name="inventory", help="Interact with inventory objects"
    )
    inventory_subparsers = inventory_parser.add_subparsers(title="subcommands", dest="inventory_action")

    # "inventory list" subcommand
    list_parser = inventory_subparsers.add_parser(name="list", help="List all inventories currently in the factory")
    list_parser.add_argument(
        "--env",
        "-e",
        required=True,
        help="The environment to list the inventories from."
    )
    list_parser.set_defaults(func=list_inventories)

    # "inventory test" subcommand
    test_parser = inventory_subparsers.add_parser(
        name="test", help="Test inventory files."
    )
    test_parser.set_defaults(func=test_inventory)

    test_parser.add_argument(
        "--env",
        "-e",
        required=True,
        help="The environment where the inventory is located"
    )

    test_parser.add_argument(
        "--inventory",
        "-i",
        required=False,
        nargs="+",
        help="The inventory to generate files from"
    )

    test_parser.add_argument(
        "--build-group",
        "-g",
        default="all",
        required=False,
        type=str,
        help="Specify a specific group to target within the inventory file"
    )

    # "inventory create" subcommand
    create_parser = inventory_subparsers.add_parser("create", help="Create a new inventory")
    create_parser.add_argument("name", help="Name of the inventory to create")

    # "inventory delete" subcommand
    delete_parser = inventory_subparsers.add_parser("delete", help="Delete an inventory")
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
        help="The environment where the inventory is located"
    )

    generate_parser.add_argument(
        "--inventory",
        "-i",
        required=False,
        nargs="+",
        help="The inventory to generate files from"
    )

    generate_parser.add_argument(
        "--build-group",
        "-g",
        default="all",
        required=False,
        type=str,
        help="Specify a specific group to target within the inventory file"
    )

    return parser

    # Create subparser for the 'create' subcommand
    # create_parser = subparsers.add_parser("create", help="Create a test environment")
    # create_parser.add_argument(
    #     "--distribution",
    #     "-d",
    #     required=True,
    #     help="Distribution name for the test environment",
    # )
    # create_parser.add_argument(
    #     "--name",
    #     "-n",
    #     required=False,
    #     help="Specify a custom name for the container. If not provided, a random name will be assigned by Docker.",
    # )
    # create_parser.add_argument(
    #     "--shell",
    #     "-s",
    #     default="/bin/bash",
    #     type=str,
    #     required=False,
    #     help="Specify a custom shell to execute inside the container. Defaults to /bin/bash",
    # )
    # create_parser.add_argument(
    #     "--connect",
    #     "-c",
    #     required=False,
    #     action="store_true",
    #     help="Connect to the created environment",
    # )
    # create_parser.add_argument(
    #     "--volume",
    #     "-v",
    #     required=False,
    #     help="Create a storage volume in the specified data path (default ~/.tangent-cli.d/) to share data with the environment.",
    #     action='store_true'
    # )
