from factory import utils
from .parser import create_parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    config = utils.load_config()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        print("Error: No command specified.")

if __name__ == "__main__":
    main()
