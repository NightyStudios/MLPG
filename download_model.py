from huggingface_hub import snapshot_download
def download_model(model: str):
    snapshot_download(repo_id=model)

