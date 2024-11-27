import os


def list_models():
    username = os.environ["USERNAME"]
    save_dir = os.path.join('C:\\Users', username, '.cache\\huggingface\\hub')
    items = os.listdir(save_dir)


    for item in items:
        if os.path.isdir(os.path.join(save_dir, item)):
            parts = item.split('--')
            if len(parts) >= 3:
                author = parts[1]
                model_name = parts[2]
                print(f"{author}/{model_name}")
            else:
                pass