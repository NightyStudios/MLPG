from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import os
import list_models


def use_model(model_name, msg, temp, topp, topk, c_size, rep_penalty, am):
    ai_class = 'None'
    pth = 'None'
    username = os.environ["USERNAME"]
    save_dir = os.path.join('C:\\Users', username, '.cache\\huggingface\\hub')

    models = list_models.list_models()
    for each in models:
        if each['model_id'] == model_name:
            ai_class = each['task']
            pth = each['path']

    if am:

        model = AutoModelForCausalLM.from_pretrained(pth, torch_dtype="auto", is_decoder=True).to("cuda")
        tokenizer = AutoTokenizer.from_pretrained(pth)

        input_ids = tokenizer(msg, return_tensors="pt").input_ids.to("cuda")
        vixlop = model.generate(input_ids, max_length=c_size, temperature=temp, top_k=topk, top_p=topp, repetition_penalty=rep_penalty, do_sample=True)
        output = tokenizer.decode(vixlop[0], skip_special_tokens=True)

    else:

        generator = pipeline(ai_class, model=pth, tokenizer=pth, device=0)
        output = generator(msg)

    return output
