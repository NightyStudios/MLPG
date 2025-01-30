import tkinter as tk
import customtkinter as ctk
import json
from list_models import list_models
from download_model import download_model
from use_model import use_model
from del_model import del_model
import tkinter.messagebox as MessageBox
from customtkinter import CTkFont  
app = ctk.CTk()
app.geometry("1920x1080")  
app.title("MLPG")

ctk.FontManager.load_font("IsamiRiDisplay-Regular.otf") # почему-то не работает


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def update_model_list():
    model_listbox.delete(0, "end")
    global models
    models = list_models()
    for model in models:
        model_id = model["model_id"]
        model_listbox.insert("end", model_id)
    app.after(1000, update_model_list)


def select_model(event):
    selected = model_listbox.get(model_listbox.curselection())
    for model in models:
        if model["model_id"] == selected:
            author, model_name = model["model_id"].split("/")
            task = model.get("task", "Unknown")
            model_name_label.configure(text=model_name.upper())
            model_type_label.configure(text=task)
            model_author_label.configure(text=author)


def install_model():
    model_name = search_entry.get()
    if model_name:
        download_model(model_name)
        update_model_list()


def send_prompt():
    prompt = prompt_entry.get()
    model_name = model_author_label.cget("text") + "/" + model_name_label.cget("text").lower()
    if prompt and model_name:
        output = use_model(model_name, prompt)
        output_textbox.delete("0.0", "end")
        output_textbox.insert("0.0", output)


def delete_selected_model():
    model_name = model_author_label.cget("text") + "/" + model_name_label.cget("text").lower()
    if model_name:
        del_model(model_name)
        update_model_list()
        MessageBox.showinfo(title="model deletion", message=f"model {model_name} has been succesfully deleted!")

model_listbox = tk.Listbox(app, width=30, font=("IsamiRiDisplay-Regular.otf", 14))
model_listbox.pack(side="left", fill="y", padx=10, pady=10)
model_listbox.bind("<<ListboxSelect>>", select_model)

search_frame = ctk.CTkFrame(app)
search_frame.pack(fill="x", padx=10, pady=5)

search_entry = ctk.CTkEntry(search_frame, placeholder_text="search and install models on Hugging Face...", font=("IsamiRiDisplay-Regular.otf", 14))
search_entry.pack(side="left", fill="x", expand=True, padx=5)

install_button = ctk.CTkButton(search_frame, text="install", font=("IsamiRiDisplay-Regular.otf", 14), command=install_model)
install_button.pack(side="right", padx=5)

model_info_frame = ctk.CTkFrame(app)
model_info_frame.pack(fill="x", padx=10, pady=5)

model_name_label = ctk.CTkLabel(model_info_frame, text="MODEL", font=("IsamiRiDisplay-Regular.otf", 14))
model_name_label.pack(side="top", fill="x", padx=5)

model_type_label = ctk.CTkLabel(model_info_frame, text="type", font=("IsamiRiDisplay-Regular.otf", 14))
model_type_label.pack(side="top", fill="x", padx=5)

model_author_label = ctk.CTkLabel(model_info_frame, text="author", font=("IsamiRiDisplay-Regular.otf", 14))
model_author_label.pack(side="top", fill="x", padx=5)

prompt_frame = ctk.CTkFrame(app)
prompt_frame.pack(fill="x", padx=10, pady=5)

prompt_entry = ctk.CTkEntry(prompt_frame, placeholder_text="please enter prompt...", font=("IsamiRiDisplay-Regular.otf", 14))
prompt_entry.pack(side="left", fill="x", expand=True, padx=5)

send_button = ctk.CTkButton(prompt_frame, text="send", font=("IsamiRiDisplay-Regular.otf", 14), command=send_prompt)
send_button.pack(side="right", padx=10, pady=5)

output_textbox = ctk.CTkTextbox(app, height=100, font=("IsamiRiDisplay-Regular.otf", 14))
output_textbox.pack(fill="both", padx=10, pady=5)

delete_button = ctk.CTkButton(app, text="delete model", font=("IsamiRiDisplay-Regular.otf", 14), command=delete_selected_model)
delete_button.pack(side="bottom", fill="x", padx=10, pady=5)

update_model_list()
app.mainloop()
