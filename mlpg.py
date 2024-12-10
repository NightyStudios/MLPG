import list_models
import download_model
import argparse
import del_model


def mlpg():
    parser = argparse.ArgumentParser(description="Playground for your ML models!")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    subparsers.add_parser("list", help="prints out all models located at C:\\Users\\{User}\\.cache\\huggingface\\hub :3")
    install_parser = subparsers.add_parser("install", help="downloads model from HF :3")
    install_parser.add_argument("name", metavar="NAME", help="specify repo_id in format author/name_of_model")
    delete_parser = subparsers.add_parser("delete", help="Deletes model and its .locks")
    delete_parser.add_argument("name", metavar="NAME", help="specify repo_id in format author/name_of_model")
    args = parser.parse_args()
    if args.command == "list":
        print("Hugging Face rules the world :3")
        print('-' * 30)
        models = list_models.list_models()
        print('\n'.join(models))
    elif args.command == "install":
        print(f"attempting to install model: {args.name}!")
        print(download_model.download_model(args.name))
    elif args.command == "delete":
        print(f"attempting to delete model: {args.name}!")
        print(del_model.del_model(args.name))

if __name__ == "__main__":
    mlpg()
