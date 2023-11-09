import argparse


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

    # "list" subcommand
    list_parser = inventory_subparsers.add_parser("list", help="List all inventories currently in the factory")
    list_parser.add_argument(
        "--env",
        "-e",
        required=True,
        help="The environment to list the inventories from."
    )
    # "create" subcommand
    create_parser = inventory_subparsers.add_parser("create", help="Create a new inventory")
    create_parser.add_argument("name", help="Name of the inventory to create")

    # "delete" subcommand
    delete_parser = inventory_subparsers.add_parser("delete", help="Delete an inventory")
    delete_parser.add_argument("name", help="Name of the inventory to delete")

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
