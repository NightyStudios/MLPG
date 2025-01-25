import os
import json
from typing import Dict, List, Optional

ARCH_TO_TASK: Dict[str, str] = {
    "ForSequenceClassification": "text-classification",
    "ForTokenClassification": "token-classification",
    "ForQuestionAnswering": "question-answering",
    "ForMultipleChoice": "multiple-choice",
    "ForCausalLM": "text-generation",
    "ForMaskedLM": "fill-mask",
    "ForConditionalGeneration": "text2text-generation",
}

def get_model_task(model_path):
    config_path = os.path.join(model_path, "config.json")
    if not os.path.exists(config_path):
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        architectures = config.get("architectures", [])
        for arch in architectures:
            for key in ARCH_TO_TASK:
                if key in arch:
                    return ARCH_TO_TASK[key]
        model_type = config.get("model_type", "")
        if model_type in ["gpt2", "bloom"]:
            return "text-generation"
        
    except Exception as e:
        print(f"smhng went wrong: {e}")
    
    return None

def list_models():
    username = os.environ["USERNAME"]
    save_dir = os.path.join('C:\\Users', username, '.cache\\huggingface\\hub')
    
    models = []
    
    for item in os.listdir(save_dir):
        item_path = os.path.join(save_dir, item)
        if os.path.isdir(item_path) and item.startswith("models--"):
            snapshots_dir = os.path.join(item_path, "snapshots")
            snapshots = os.listdir(snapshots_dir)
            latest_snapshot = os.path.join(snapshots_dir, snapshots[-1])
            task = get_model_task(latest_snapshot)
            
            parts = item.split("--")
            if len(parts) >= 3:
                author = parts[1]
                model_name = "--".join(parts[2:])  
                models.append({"model_id": f"{author}/{model_name}", "task": task or "no info", 'path': latest_snapshot})
    
    return models