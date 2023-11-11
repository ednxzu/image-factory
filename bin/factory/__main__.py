from .parser import create_parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("Error: No command specified.")


if __name__ == "__main__":
    main()
