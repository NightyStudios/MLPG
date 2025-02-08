import tkinter as tk
import customtkinter as ctk

from list_models import list_models
from download_model import download_model
from use_model import use_model
from del_model import del_model
import tkinter.messagebox as MessageBox

app = ctk.CTk()
app.geometry("1920x1080")
app.title("MLPG")

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

    try:
        params = {
            "temp": float(temp_entry.get()) if temp_entry.get() else 1.0,
            "topk": int(top_k_entry.get()) if top_k_entry.get() else 50,
            "topp": float(top_p_entry.get()) if top_p_entry.get() else 1.0,
            "c_size": int(max_length_entry.get()) if max_length_entry.get() else 512,
            "rep_penalty": float(repetition_penalty_entry.get()) if repetition_penalty_entry.get() else 1.0,
            "am": bool(am_entry.get()) if am_entry.get() else False,
        }
    except ValueError:
        MessageBox.showerror("that's an error!", "please check specified parameters")
        return

    if prompt and model_name:
        output = use_model(model_name, prompt, **params)
        output_textbox.delete("0.0", "end")
        output_textbox.insert("0.0", output)


def delete_selected_model():
    model_name = model_author_label.cget("text") + "/" + model_name_label.cget("text").lower()
    if model_name:
        del_model(model_name)
        update_model_list()
        MessageBox.showinfo(title="delete model", message=f"model {model_name} has been succesfully deleted!")


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

        # Set default values
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


model_listbox = tk.Listbox(app, width=30, font=("Arial", 14))
model_listbox.pack(side="left", fill="y", padx=10, pady=10)
model_listbox.bind("<<ListboxSelect>>", select_model)

search_frame = ctk.CTkFrame(app)
search_frame.pack(fill="x", padx=10, pady=5)

search_entry = ctk.CTkEntry(search_frame, placeholder_text="enter model name...", font=("Arial", 14))
search_entry.pack(side="left", fill="x", expand=True, padx=5)

install_button = ctk.CTkButton(search_frame, text="install", font=("Arial", 14), command=install_model)
install_button.pack(side="right", padx=5)

model_info_frame = ctk.CTkFrame(app)
model_info_frame.pack(fill="x", padx=10, pady=5)

model_name_label = ctk.CTkLabel(model_info_frame, text="MODEL", font=("Arial", 14))
model_name_label.pack(side="top", fill="x", padx=5)

model_type_label = ctk.CTkLabel(model_info_frame, text="Тип", font=("Arial", 14))
model_type_label.pack(side="top", fill="x", padx=5)

model_author_label = ctk.CTkLabel(model_info_frame, text="Автор", font=("Arial", 14))
model_author_label.pack(side="top", fill="x", padx=5)

prompt_frame = ctk.CTkFrame(app)
prompt_frame.pack(fill="x", padx=10, pady=5)

prompt_entry = ctk.CTkEntry(prompt_frame, placeholder_text="enter prompt...", font=("Arial", 14))
prompt_entry.pack(side="left", fill="x", expand=True, padx=5)

send_button = ctk.CTkButton(prompt_frame, text="send", font=("Arial", 14), command=send_prompt)
send_button.pack(side="right", padx=10, pady=5)

params_frame = ctk.CTkFrame(app)
params_frame.pack(fill="x", padx=10, pady=5)

ctk.CTkLabel(params_frame, text="use advanced mode?", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
am_entry = ctk.CTkCheckBox(params_frame, text="enable", font=("Arial", 14), command=toggle_advanced_mode)
am_entry.grid(row=0, column=1, padx=5, pady=5)

temp_label = ctk.CTkLabel(params_frame, text="temperature:", font=("Arial", 14))
top_k_label = ctk.CTkLabel(params_frame, text="top-k:", font=("Arial", 14))
top_p_label = ctk.CTkLabel(params_frame, text="top-p:", font=("Arial", 14))
repetition_penalty_label = ctk.CTkLabel(params_frame, text="repetition penalty:", font=("Arial", 14))
max_length_label = ctk.CTkLabel(params_frame, text="max length:", font=("Arial", 14))

temp_entry = ctk.CTkEntry(params_frame, font=("Arial", 14))
top_k_entry = ctk.CTkEntry(params_frame, font=("Arial", 14))
top_p_entry = ctk.CTkEntry(params_frame, font=("Arial", 14))
repetition_penalty_entry = ctk.CTkEntry(params_frame, font=("Arial", 14))
max_length_entry = ctk.CTkEntry(params_frame, font=("Arial", 14))

output_textbox = ctk.CTkTextbox(app, height=200, font=("Arial", 14))
output_textbox.pack(fill="both", padx=10, pady=5)

delete_button = ctk.CTkButton(app, text="delete model", font=("Arial", 14), command=delete_selected_model)
delete_button.pack(side="bottom", fill="x", padx=10, pady=5)

update_model_list()
app.mainloop()
