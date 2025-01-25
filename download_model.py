import os
from huggingface_hub import snapshot_download
global path

username = os.environ["USERNAME"]
path = os.path.join('C:\\Users', username, '.cache\\huggingface\\hub')

def download_model(model: str):
    global path 
    snapshot_download(repo_id = model, cache_dir = path)

