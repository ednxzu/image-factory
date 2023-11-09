from factory import utils
from .functions.general_utils import list_inventories, create_inventory, delete_inventory
from .parser import create_parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    config = utils.load_config()

    if args.action == "inventory":
        print(args)
        if args.inventory_action == "list":
            list_inventories(config['inventory_path'], args.env)

if __name__ == "__main__":
    main()
