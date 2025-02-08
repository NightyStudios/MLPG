import argparse
from list_models import list_models
import download_model
import del_model
import use_model


def mlpg():
    parser = argparse.ArgumentParser(description="Playground for your ML models!")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    subparsers.add_parser("list",
                          help="prints out all models located at C:\\Users\\{User}\\.cache\\huggingface\\hub :3")

    install_parser = subparsers.add_parser("install", help="download a model from HF")
    install_parser.add_argument("name", metavar="NAME", help="specify repo_id in format author/name_of_model")

    delete_parser = subparsers.add_parser("delete", help="deletes model and its .locks")
    delete_parser.add_argument("name", metavar="NAME", help="specify repo_id in format author/name_of_model")

    use_parser = subparsers.add_parser("use", help="use a model to process text")
    use_parser.add_argument("model_id", metavar="MODEL_ID", help="specify model_id to use")
    use_parser.add_argument("--temp", type=float, default=1.0, help="temperature (a.k.a 'creativity')")
    use_parser.add_argument("--top_p", type=float, default=1.0, help="top-p (nucleus sampling)")
    use_parser.add_argument("--top_k", type=int, default=50, help="top-k sampling")
    use_parser.add_argument("--context_size", type=int, default=512, help="maximum context size")
    use_parser.add_argument("--basic", action="store_true", help="use pipeline (basic mode)")
    use_parser.add_argument("--advanced", action="store_true", help="use manual tweaking (advanced mode)")

    args = parser.parse_args()

    if args.command == "list":
        print("AI rules the world! \nYour installed models:")
        print('-' * 30)
        models = list_models()
        for model in models:
            print(f"model: {model['model_id']}")
            print(f"type: {model['task']}")
            print('-' * 30)
    elif args.command == "install":
        print(f"attempting to install model: {args.name}!")
        result = download_model.download_model(args.name)
        print(result)
    elif args.command == "delete":
        print(f"attempting to delete model: {args.name}!")
        result = del_model.del_model(args.name)
        print(result)
    elif args.command == "use":
        print(f"using model: {args.model_id}")
        print(f"parameters:\ntemperature: {args.temp},\nTop-p: {args.top_p},\nTop-k: {args.top_k},\ncontext size: {args.context_size}")

        msg = input("Please enter model prompt here -> ")

        if args.basic:
            print("running in basic mode using pipeline...")
            result = use_model.use_model(args.model_id, msg, args.temp, args.top_p, args.top_k, args.context_size, rep_penalty=1.0, am=False)
        elif args.advanced:
            print("running in advanced mode using manual model tweaking...")
            result = use_model.use_model(args.model_id, msg, args.temp, args.top_p, args.top_k, args.context_size, rep_penalty=1.0, am=True)
        else:
            print("no mode specified, defaulting to basic mode...")
            result = use_model.use_model(args.model_id, msg, args.temp, args.top_p, args.top_k, args.context_size, rep_penalty=1.0, am=False)

        print("model returned:", result)


if __name__ == "__main__":
    mlpg()
