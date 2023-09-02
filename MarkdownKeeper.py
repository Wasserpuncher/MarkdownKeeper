import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
from datetime import datetime

# Funktion zur Erstellung von Notizen

def create_new_note():
    title = title_entry.get()
    content = content_text.get("1.0", tk.END)
    
    # Überprüfen, ob ein Hauptordner ausgewählt wurde
    if not note_directory:
        status_label.config(text="Bitte wählen Sie zuerst einen Hauptordner aus.")
        return
    
    # Überprüfen, ob der Hauptordner bereits existiert. Andernfalls erstellen Sie ihn.
    if not os.path.exists(note_directory):
        os.makedirs(note_directory)
    
    # Erstellen eines Unterordners mit dem aktuellen Datum
    current_date = datetime.now().strftime("%Y-%m-%d")
    date_folder = os.path.join(note_directory, current_date)
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)
    
    # Erstellen Sie den Dateipfad für die neue Notiz
    note_path = os.path.join(date_folder, f"{title}.md")
    
    # Erstellen Sie die Markdown-Datei und speichern Sie den Inhalt
    with open(note_path, "w") as file:
        file.write(content)
    
    clear_fields()
    status_label.config(text="Notiz wurde erstellt und gespeichert.")
    update_note_list()

def clear_fields():
    title_entry.delete(0, tk.END)
    content_text.delete("1.0", tk.END)

def choose_directory():
    global note_directory
    note_directory = filedialog.askdirectory()
    status_label.config(text=f"Hauptordner ausgewählt: {note_directory}")
    update_note_list()

def update_note_list():
    note_listbox.delete(0, tk.END)
    if note_directory:
        for root, dirs, files in os.walk(note_directory):
            for file in files:
                note_listbox.insert(tk.END, os.path.relpath(os.path.join(root, file), note_directory))

def open_note():
    selected_note = note_listbox.get(note_listbox.curselection())
    with open(os.path.join(note_directory, selected_note), "r") as file:
        content = file.read()
    clear_fields()
    title_entry.insert(0, os.path.splitext(selected_note)[0])
    content_text.insert(tk.END, content)

def delete_note():
    selected_note = note_listbox.get(note_listbox.curselection())
    result = messagebox.askyesno("Notiz löschen", f"Möchten Sie die Notiz '{selected_note}' wirklich löschen?")
    if result:
        os.remove(os.path.join(note_directory, selected_note))
        clear_fields()
        status_label.config(text=f"Notiz '{selected_note}' wurde gelöscht.")
        update_note_list()

def change_font_size():
    font_size = font_size_var.get()
    content_text.config(font=(current_font_family, font_size))

def change_font_family():
    font_family = font_family_var.get()
    content_text.config(font=(font_family, current_font_size))

# Erstellen des Hauptfensters

root = tk.Tk()
root.title("MarkdownKeeper")

# GUI-Elemente

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

main_folder_label = tk.Label(frame, text="Hauptordner auswählen:")
main_folder_label.grid(row=0, column=0, sticky="w")

main_folder_button = tk.Button(frame, text="Hauptordner auswählen", command=choose_directory)
main_folder_button.grid(row=0, column=1, padx=10, pady=5)

main_folder_name_label = tk.Label(frame, text="Name des Hauptordners:")
main_folder_name_label.grid(row=1, column=0, sticky="w")

main_folder_name_entry = tk.Entry(frame)
main_folder_name_entry.grid(row=1, column=1, padx=10, pady=5)

title_label = tk.Label(frame, text="Titel der Notiz:")
title_label.grid(row=2, column=0, sticky="w")

title_entry = tk.Entry(frame)
title_entry.grid(row=2, column=1, padx=10, pady=5)

content_label = tk.Label(frame, text="Inhalt der Notiz (in Markdown-Syntax):")
content_label.grid(row=3, column=0, sticky="w")

content_text = tk.Text(frame, height=10, width=40)
content_text.grid(row=3, column=1, padx=10, pady=5)

create_button = tk.Button(frame, text="Notiz erstellen", command=create_new_note)
create_button.grid(row=4, column=0, columnspan=2, pady=10)

clear_button = tk.Button(frame, text="Felder löschen", command=clear_fields)
clear_button.grid(row=5, column=0, columnspan=2, pady=5)

status_label = tk.Label(root, text="", font=("Helvetica", 12))
status_label.pack(pady=10)

# Variable für den ausgewählten Hauptordner

note_directory = ""
main_folder_name = ""

# Notizliste anzeigen

list_frame = tk.Frame(root)
list_frame.pack(padx=20, pady=10)

note_list_label = tk.Label(list_frame, text="Notizen:")
note_list_label.grid(row=0, column=0, sticky="w")

note_listbox = tk.Listbox(list_frame, height=5, width=50)
note_listbox.grid(row=1, column=0, padx=10, pady=5)

note_list_scroll = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
note_list_scroll.config(command=note_listbox.yview)
note_list_scroll.grid(row=1, column=1, sticky="ns")

note_listbox.config(yscrollcommand=note_list_scroll.set)

update_note_list()

open_button = tk.Button(list_frame, text="Notiz öffnen", command=open_note)
open_button.grid(row=2, column=0, padx=10, pady=5)

delete_button = tk.Button(list_frame, text="Notiz löschen", command=delete_note)
delete_button.grid(row=2, column=1, padx=10, pady=5)

# Schriftgröße und Schriftart

font_frame = tk.Frame(root)
font_frame.pack(padx=20, pady=10)

font_size_label = tk.Label(font_frame, text="Schriftgröße:")
font_size_label.grid(row=0, column=0, sticky="w")

font_size_var = tk.StringVar()
font_size_var.set(12)  # Standard-Schriftgröße

font_size_entry = tk.Entry(font_frame, textvariable=font_size_var, width=5)
font_size_entry.grid(row=0, column=1, padx=10, pady=5)

font_size_button = tk.Button(font_frame, text="Ändern", command=change_font_size)
font_size_button.grid(row=0, column=2, padx=10, pady=5)

font_family_label = tk.Label(font_frame, text="Schriftart:")
font_family_label.grid(row=1, column=0, sticky="w")

font_family_var = tk.StringVar()

font_families = [
    "Arial",
    "Helvetica",
    "Times New Roman",
    "Courier New",
    "Verdana",
]

font_family_var.set(font_families[0])  # Standard-Schriftart

font_family_menu = tk.OptionMenu(font_frame, font_family_var, *font_families)
font_family_menu.grid(row=1, column=1, padx=10, pady=5)

font_family_button = tk.Button(font_frame, text="Ändern", command=change_font_family)
font_family_button.grid(row=1, column=2, padx=10, pady=5)

# Aktuelle Schriftgröße und Schriftart

current_font_size = int(font_size_var.get())
current_font_family = font_family_var.get()

# Hauptloop starten

root.mainloop()
