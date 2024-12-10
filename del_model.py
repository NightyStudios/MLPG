import os
import shutil

def del_model(model):
    username = os.environ["USERNAME"]
    model_dir = os.path.join('C:\\Users', username, '.cache\\huggingface\\hub')
    locks_dir = os.path.join('C:\\Users', username, '.cache\\huggingface\\hub\\.locks')
    model_parts = model.split('/')
    author, name = model_parts
    folder_name = f"models--{author}--{name}"
    model_dir = os.path.join(model_dir, folder_name)
    locks_dir = os.path.join(locks_dir, folder_name)
    msg = []
    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)
        msg.append(f"Deleted model: {model_dir} :3")
    else:
        msg.append(f"Couldn't find: {model_dir} :(")
    if os.path.exists(locks_dir):
        shutil.rmtree(locks_dir)
        msg.append(f"Deleted .locks: {locks_dir} :3")
    else:
        msg.append(f".locks folder not found: {locks_dir} :(")

    return "\n".join(msg)
