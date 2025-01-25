import argparse
from list_models import list_models 
import download_model
import del_model
import use_model

def mlpg():
    parser = argparse.ArgumentParser(description="Playground for your ML models!")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    
    subparsers.add_parser("list", help="prints out all models located at C:\\Users\\{User}\\.cache\\huggingface\\hub :3")
    
    install_parser = subparsers.add_parser("install", help="downloads model from HF :3")
    install_parser.add_argument("name", metavar="NAME", help="specify repo_id in format author/name_of_model")
    
    delete_parser = subparsers.add_parser("delete", help="deletes model and its .locks")
    delete_parser.add_argument("name", metavar="NAME", help="specify repo_id in format author/name_of_model")
    
    use_parser = subparsers.add_parser("use", help="Use a model to process text")
    use_parser.add_argument("model_id", metavar="MODEL_ID", help="specify model_id to use")
    
    args = parser.parse_args()
    
    if args.command == "list":
        print("Hugging Face rules the world :3")
        print('-' * 30)
        models = list_models()
        for model in models:
            print(f"model: {model['model_id']}")
            print(f"type: {model['task']}")
            print('-' * 30)
    elif args.command == "install":
        print(f"Attempting to install model: {args.name}!")
        result = download_model.download_model(args.name)
        print(result)
    elif args.command == "delete":
        print(f"Attempting to delete model: {args.name}!")
        result = del_model.del_model(args.name)
        print(result)
    elif args.command == "use":
        print(f"Using model: {args.model_id}")
        msg = input("Please enter model prompt here -> ")
        result = use_model.use_model(args.model_id, msg)
        print("Model returnd:", result)

if __name__ == "__main__":
    mlpg()