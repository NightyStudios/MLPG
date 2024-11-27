from transformers import AutoModel, AutoTokenizer

def load_model(model_name: str):
    """
    Загрузка модели и токенизатора с Hugging Face.

    :param model_name: Название модели на Hugging Face (например, 'bert-base-uncased').
    :return: Кортеж (модель, токенизатор)
    """
    try:
        # Загрузка токенизатора
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Загрузка модели
        model = AutoModel.from_pretrained(model_name)
        print(f"Модель '{model_name}' успешно загружена!")
        return model, tokenizer
    except Exception as e:
        print(f"Ошибка при загрузке модели '{model_name}': {e}")
        return None, None


# Пример использования
if __name__ == "__main__":
    model_name = "papluca/xlm-roberta-base-language-detection"  # Укажите нужное имя модели
    model, tokenizer = load_model(model_name)
