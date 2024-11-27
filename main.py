import list_models
import download_model
import argparse



def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Model management utility.')

    # Create a mutually exclusive group for the arguments
    group = parser.add_mutually_exclusive_group(required=True)

    # Add --list-models argument
    group.add_argument('--list-models', action='store_true', help='List all available models.')

    # Add --get-model argument
    group.add_argument('--get-model', metavar='NAME', help='Get details of a specific model.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the appropriate function based on the arguments
    if args.list_models:
        list_models.list_models()
    elif args.get_model:
        download_model.download_model(args.get_model)


if __name__ == '__main__':
    main()