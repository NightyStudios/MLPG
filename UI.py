import os
import threading
import tkinter as tk
import tkinter.messagebox as MessageBox

import customtkinter as ctk
import markdown2
from PIL import Image
from tkinterweb import HtmlFrame
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer, MBartForConditionalGeneration, MBart50TokenizerFast

from del_model import del_model
from download_model import download_model
from list_models import list_models
from use_model import use_model

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary_cache = {}

model_name = "TheTEm/mbart-itlang-finetuned"


model = MBartForConditionalGeneration.from_pretrained(model_name)
tokenizer = MBart50TokenizerFast.from_pretrained(model_name)

src_lang = "en_XX"
tgt_lang = "ru_RU"
tokenizer.src_lang = src_lang
tokenizer.tgt_lang = tgt_lang


def split_text(text, max_chars=1000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]


def summarize_and_translate(text):
    if text in summary_cache:
        return summary_cache[text]

    max_chars = 1000

    if len(text) > max_chars:
        chunks = split_text(text, max_chars)
        chunk_summaries = []
        for chunk in chunks:
            summary = summarizer(chunk, max_length=18, min_length=1, do_sample=False)[0]['summary_text']
            chunk_summaries.append(summary)
        full_summary = " ".join(chunk_summaries)
    else:
        full_summary = summarizer(text, max_length=18, min_length=1, do_sample=False)[0]['summary_text']


    inputs = tokenizer(full_summary, return_tensors="pt", padding=True, truncation=True)


    generated_tokens = model.generate(inputs["input_ids"], max_length=128)


    translation = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
    summary_cache[text] = translation
    return translation


def process_summarization_async(text, widget):
    def worker():
        try:
            result = summarize_and_translate(text)
        except Exception as e:
            result = f"Ой, что-то сломалось: {e}"
        app.after(0, lambda: widget.load_html("<p>" + result + "</p>" + dark_mode_styles))

    threading.Thread(target=worker, daemon=True).start()


dark_mode_styles = """
    <style>
        body {
            background-color: #1d1d1e;
            color: #dce4ee;
            font-family: Arial, sans-serif;
        }
        pre, code {
            background-color: #333333;
            color: #dce4ee;
            padding: 5px;
            border-radius: 3px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #dce4ee;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        a {
            color: #dce4ee;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
"""


def show_tutorial():
    tutorial_window = ctk.CTkToplevel(app)
    tutorial_window.title("Обучение")
    tutorial_window.geometry("1200x900")
    tutorial_window.resizable(False, False)
    tutorial_window.transient(app)
    tutorial_window.grab_set()
    app.attributes("-alpha", 1.0)

    def on_close():
        app.attributes("-alpha", 1.0)
        tutorial_window.grab_release()
        tutorial_window.destroy()

    tutorial_window.protocol("WM_DELETE_WINDOW", on_close)
    tutorial_steps = [{
        "text": "Добро пожаловать в MLPG - песочницу для моделей ИИ! \n В этой инструкции вы узнаете, как пользоваться приложением и использовать ИИ на всю мощь!",
        "image": r"src\logo.png"}, {
        "text": "В верхней поисковой строке вы можете ввести название модели в формате автор/имя и программа скачает её с Hugging Face, например openai-community/gpt2",
        "image": r"src\download.png"},
        {"text": "Загруженные модели отображаются в списке слева", "image": r"src\list.png"}, {
            "text": "Чтобы использовать модель, выберите её из списка. Ее характеристики (имя, тип и автор) отобразятся на основном экране (1). \n В текстовом поле (2) введите запрос для модели и нажмите на кнопку отправки (3) \n Результат отобразится в поле ниже (4)",
            "image": r"src\basic.png"}, {
            "text": "Для использования продвинутых настроек нужно включить флажок (1) и настроить параметры (2) \n Затем, как в предыдущем пункте, нажать кнопку (3)",
            "image": r"src\advanced.png"}, {
            "text": "Температура (temperature) — параметр, который контролирует степень случайности в ответах модели. Низкая температура делает ответы более предсказуемыми, а высокая – разнообразными",
            "image": r"src\temp.png"},
        {"text": "Top-k (первые k) выбирает k наиболее вероятных слов, увеличивая разнообразие ответов",
            "image": r"src\top-k.png"}, {
            "text": "Top-p (nucleus sampling) следит, чтобы сумма вероятностей не превышала p, позволяя модели использовать более широкий словарь",
            "image": r"src\top-p.png"},
        {"text": "Наказание за повтор (repetition penalty) снижает вероятность повторения слов в ответе",
            "image": r"src\rep.png"},
        {"text": "Кол-во токенов регулирует максимальную длину вывода модели", "image": r"src\lengh.png"},
        {"text": "Для оптимизации дискового пространства вы можете удалить использованные модели",
            "image": r"src\del.png"},
        {"text": "Теперь вы знаете все для старта! Желаем успехов и приятного пользования!",
            "image": r"src\logo.png"}, ]
    tutorial_window.tutorial_steps = tutorial_steps
    tutorial_window.current_step = 0

    tutorial_image_label = ctk.CTkLabel(tutorial_window, text="")
    tutorial_image_label.pack(pady=10)

    tutorial_text_label = ctk.CTkLabel(tutorial_window, text="", wraplength=1100, font=('Arial', 25))
    tutorial_text_label.pack(pady=5)

    button_frame = ctk.CTkFrame(tutorial_window)
    button_frame.pack(side="bottom", fill="x", pady=10)

    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)

    tutorial_prev_button = ctk.CTkButton(button_frame, text="←",
        command=lambda: tutorial_prev_step(tutorial_window, tutorial_image_label, tutorial_text_label,
                                           tutorial_prev_button, tutorial_next_button), state="disabled",
        font=('Arial', 30))
    tutorial_prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    tutorial_close_button = ctk.CTkButton(button_frame, text="Закрыть", command=on_close, font=('Arial', 30))
    tutorial_close_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    tutorial_next_button = ctk.CTkButton(button_frame, text="→",
        command=lambda: tutorial_next_step(tutorial_window, tutorial_image_label, tutorial_text_label,
                                           tutorial_prev_button, tutorial_next_button), font=('Arial', 30))
    tutorial_next_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    update_tutorial_step(tutorial_window, tutorial_image_label, tutorial_text_label, tutorial_prev_button,
                         tutorial_next_button)


def update_tutorial_step(tutorial_window, tutorial_image_label, tutorial_text_label, tutorial_prev_button,
                         tutorial_next_button):
    step = tutorial_window.tutorial_steps[tutorial_window.current_step]
    tutorial_text_label.configure(text=step["text"])
    image = ctk.CTkImage(light_image=Image.open(step["image"]), size=(1000, 600))
    tutorial_image_label.configure(image=image)
    tutorial_image_label.image = image
    tutorial_prev_button.configure(state="normal" if tutorial_window.current_step > 0 else "disabled")
    tutorial_next_button.configure(
        text="Готово" if tutorial_window.current_step == len(tutorial_window.tutorial_steps) - 1 else "→")


def tutorial_next_step(tutorial_window, tutorial_image_label, tutorial_text_label, tutorial_prev_button,
                       tutorial_next_button):
    if tutorial_window.current_step < len(tutorial_window.tutorial_steps) - 1:
        tutorial_window.current_step += 1
        update_tutorial_step(tutorial_window, tutorial_image_label, tutorial_text_label, tutorial_prev_button,
                             tutorial_next_button)
    else:
        app.attributes("-alpha", 1.0)
        tutorial_window.grab_release()
        tutorial_window.destroy()


def tutorial_prev_step(tutorial_window, tutorial_image_label, tutorial_text_label, tutorial_prev_button,
                       tutorial_next_button):
    if tutorial_window.current_step > 0:
        tutorial_window.current_step -= 1
        update_tutorial_step(tutorial_window, tutorial_image_label, tutorial_text_label, tutorial_prev_button,
                             tutorial_next_button)


app = ctk.CTk()
app.geometry("1920x1080")
app.title("MLPG")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
show_tutorial()

model_listbox = tk.Listbox(app, width=30, font=("Arial", 25))
model_listbox.pack(side="left", fill="y", padx=10, pady=10)
model_listbox.bind("<<ListboxSelect>>", lambda event: select_model(event))

search_frame = ctk.CTkFrame(app)
search_frame.pack(fill="x", padx=10, pady=5)

search_entry = ctk.CTkEntry(search_frame, placeholder_text="введите название модели для скачивания...",
                            font=("Arial", 25))
search_entry.pack(side="left", fill="x", expand=True, padx=5)
install_button = ctk.CTkButton(search_frame, text="скачать", font=("Arial", 25), command=lambda: install_model())
install_button.pack(side="right", padx=5)

model_info_frame = ctk.CTkFrame(app)
model_info_frame.pack(fill="x", padx=10, pady=5)

model_name_label = ctk.CTkLabel(model_info_frame, text="ИМЯ", font=("Arial", 25))
model_name_label.pack(side="top", fill="x", padx=5)
model_type_label = ctk.CTkLabel(model_info_frame, text="Тип", font=("Arial", 25))
model_type_label.pack(side="top", fill="x", padx=5)
model_author_label = ctk.CTkLabel(model_info_frame, text="Автор", font=("Arial", 25))
model_author_label.pack(side="top", fill="x", padx=5)

prompt_frame = ctk.CTkFrame(app)
prompt_frame.pack(fill="x", padx=10, pady=5)

prompt_entry = ctk.CTkEntry(prompt_frame, placeholder_text="введите промпт...", font=("Arial", 25))
prompt_entry.pack(side="left", fill="x", expand=True, padx=5)
send_button = ctk.CTkButton(prompt_frame, text="отправить", font=("Arial", 25), command=lambda: send_prompt())
send_button.pack(side="right", padx=10, pady=5)

params_frame = ctk.CTkFrame(app)
params_frame.pack(fill="x", padx=10, pady=5)

ctk.CTkLabel(params_frame, text="продвинутый режим", font=("Arial", 25)).grid(row=0, column=0, padx=5, pady=5)
am_entry = ctk.CTkCheckBox(params_frame, text="включить", font=("Arial", 25), command=lambda: toggle_advanced_mode())
am_entry.grid(row=0, column=1, padx=5, pady=5)

temp_label = ctk.CTkLabel(params_frame, text="температура:", font=("Arial", 25))
top_k_label = ctk.CTkLabel(params_frame, text="top-k:", font=("Arial", 25))
top_p_label = ctk.CTkLabel(params_frame, text="top-p:", font=("Arial", 25))
repetition_penalty_label = ctk.CTkLabel(params_frame, text="наказание за повтор:", font=("Arial", 25))
max_length_label = ctk.CTkLabel(params_frame, text="кол-во токенов:", font=("Arial", 25))

temp_entry = ctk.CTkEntry(params_frame, font=("Arial", 25))
top_k_entry = ctk.CTkEntry(params_frame, font=("Arial", 25))
top_p_entry = ctk.CTkEntry(params_frame, font=("Arial", 25))
repetition_penalty_entry = ctk.CTkEntry(params_frame, font=("Arial", 25))
max_length_entry = ctk.CTkEntry(params_frame, font=("Arial", 25))

output_textbox = ctk.CTkTextbox(app, height=200, font=("Arial", 25))
output_textbox.pack(fill="both", padx=10, pady=5)

readme_summary_frame = ctk.CTkFrame(app)
readme_summary_frame.pack(fill="both", expand=True, padx=10, pady=5)

readme_frame = ctk.CTkFrame(readme_summary_frame)
readme_frame.grid(row=0, column=0, sticky="nsew", padx=5)
readme_label = ctk.CTkLabel(readme_frame, text="README.md", font=("Arial", 25))
readme_label.pack(anchor="w", padx=5, pady=5)
readme_textbox = HtmlFrame(readme_frame, horizontal_scrollbar="auto")
readme_textbox.pack(fill="both", expand=True, padx=5, pady=5)

summary_frame = ctk.CTkFrame(readme_summary_frame)
summary_frame.grid(row=0, column=1, sticky="nsew", padx=5)
summary_label = ctk.CTkLabel(summary_frame, text="Кратко о модели", font=("Arial", 25))
summary_label.pack(anchor="w", padx=5, pady=5)
summary_textbox = HtmlFrame(summary_frame, horizontal_scrollbar="auto")
summary_textbox.pack(fill="both", expand=True, padx=5, pady=5)

readme_summary_frame.grid_columnconfigure(0, weight=1)
readme_summary_frame.grid_columnconfigure(1, weight=1)


def load_readme(model_name):
    selected = model_listbox.get(model_listbox.curselection())
    for model in models:
        if model["model_id"] == selected:
            readme_path = os.path.join(model.get("path"), "README.md")
            if os.path.exists(readme_path):
                with open(readme_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return content
            return "README.md не найден."


def update_model_list():
    model_listbox.delete(0, "end")
    global models
    models = list_models()
    for model in models:
        model_id = model["model_id"]
        model_listbox.insert("end", model_id)
    app.after(1000, update_model_list)


def select_model(event):
    try:
        selected = model_listbox.get(model_listbox.curselection())
    except tk.TclError:
        return

    for model in models:
        if model["model_id"] == selected:
            author, model_name = model["model_id"].split("/")
            task = model.get("task", "Неизвестно")

            model_name_label.configure(text=model_name.upper())
            model_type_label.configure(text=task)
            model_author_label.configure(text=author)

            readme_content = load_readme(model["model_id"])
            if readme_content:
                readme_html = markdown2.markdown(readme_content, extras=["fenced-code-blocks"]).replace("\n", "\n\n")
                readme_textbox.load_html(readme_html + dark_mode_styles)
                # Асинхронная обработка суммаризации и перевода
                process_summarization_async(readme_content, summary_textbox)
            else:
                readme_textbox.load_html("<p>README.md не найден.</p>")
                summary_textbox.load_html("<p>Нет данных для суммаризации.</p>")


def install_model():
    model_name = search_entry.get()
    if model_name:
        download_model(model_name)
        update_model_list()


def send_prompt():
    prompt = prompt_entry.get()
    model_name = model_author_label.cget("text") + "/" + model_name_label.cget("text").lower()

    try:
        params = {"temp": float(temp_entry.get()) if temp_entry.get() else 1.0,
            "topk": int(top_k_entry.get()) if top_k_entry.get() else 50,
            "topp": float(top_p_entry.get()) if top_p_entry.get() else 1.0,
            "c_size": int(max_length_entry.get()) if max_length_entry.get() else 512,
            "rep_penalty": float(repetition_penalty_entry.get()) if repetition_penalty_entry.get() else 1.0,
            "am": bool(am_entry.get()) if am_entry.get() else False, }
    except ValueError:
        MessageBox.showerror("возникла ошибка!", "пожалуйста, проверь указанные параметры")
        return

    if prompt and model_name:
        output = use_model(model_name, prompt, params["temp"], params["topp"], params["topk"], params["c_size"],
                           params["rep_penalty"], params["am"])
        output_textbox.delete("0.0", "end")
        output_textbox.insert("0.0", output)


def delete_selected_model():
    model_name = model_author_label.cget("text") + "/" + model_name_label.cget("text").lower()
    if model_name:
        del_model(model_name)
        update_model_list()
        MessageBox.showinfo(title="удаление", message=f"модель {model_name} удалена без происшествий!")


def toggle_advanced_mode():
    if am_entry.get():
        temp_label.grid(row=1, column=0, padx=5, pady=5)
        temp_entry.grid(row=1, column=1, padx=5, pady=5)
        top_k_label.grid(row=2, column=0, padx=5, pady=5)
        top_k_entry.grid(row=2, column=1, padx=5, pady=5)
        top_p_label.grid(row=3, column=0, padx=5, pady=5)
        top_p_entry.grid(row=3, column=1, padx=5, pady=5)
        repetition_penalty_label.grid(row=4, column=0, padx=5, pady=5)
        repetition_penalty_entry.grid(row=4, column=1, padx=5, pady=5)
        max_length_label.grid(row=5, column=0, padx=5, pady=5)
        max_length_entry.grid(row=5, column=1, padx=5, pady=5)
        temp_entry.delete(0, "end")
        temp_entry.insert(0, "1.0")
        top_k_entry.delete(0, "end")
        top_k_entry.insert(0, "50")
        top_p_entry.delete(0, "end")
        top_p_entry.insert(0, "1.0")
        repetition_penalty_entry.delete(0, "end")
        repetition_penalty_entry.insert(0, "1.0")
        max_length_entry.delete(0, "end")
        max_length_entry.insert(0, "512")
    else:
        temp_label.grid_forget()
        temp_entry.grid_forget()
        top_k_label.grid_forget()
        top_k_entry.grid_forget()
        top_p_label.grid_forget()
        top_p_entry.grid_forget()
        repetition_penalty_label.grid_forget()
        repetition_penalty_entry.grid_forget()
        max_length_label.grid_forget()
        max_length_entry.grid_forget()


delete_button = ctk.CTkButton(app, text="удалить модель", font=("Arial", 25), command=delete_selected_model,
                              fg_color="#DB2748", hover_color="#BA2020")
delete_button.pack(side="bottom", fill="x", padx=10, pady=5)

update_model_list()
app.mainloop()
