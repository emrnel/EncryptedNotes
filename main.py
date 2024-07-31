import tkinter as tk
import base64
import os

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

salt = os.urandom(16)


def generate_key(master_key):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_key.encode()))


def encrypt(msg, master_key):
    key = generate_key(master_key)
    f = Fernet(key)
    return f.encrypt(msg.encode())


def decrypt(token, master_key):
    key = generate_key(master_key)
    f = Fernet(key)
    try:
        return f.decrypt(token).decode()
    except cryptography.fernet.InvalidToken:
        return "Invalid password or corrupted message"


def save_to_file():
    title = enter_title.get()
    secret_text = enter_secret.get(1.0, tk.END).strip()
    master_key = enter_master_key.get()
    encrypted_text = encrypt(secret_text, master_key)
    with open("note.txt", "a") as note_file:
        note_file.write(f"title: {title}\n")
        note_file.write(f"{encrypted_text.decode()}\n")


def decrypt_file():
    title = enter_title.get()
    master_key = enter_master_key.get()
    with open("note.txt", "r") as note_file:
        lines = note_file.readlines()
    token = None
    for i in range(len(lines)):
        if lines[i].strip() == f"title: {title}":
            token = lines[i + 1].strip().encode()
            break
    if token:
        decrypted_text = decrypt(token, master_key)
        enter_secret.delete(1.0, tk.END)
        enter_secret.insert(tk.END, decrypted_text)
    else:
        enter_secret.delete(1.0, tk.END)
        enter_secret.insert(tk.END, "Title not found")


# Create the main window
window = tk.Tk()
window.config(padx=5, pady=5)
window.title("Encrypted Notes")
window.geometry("300x500")

# Load the image
image = tk.PhotoImage(file="topsecret.png")
image = image.subsample(6, 6)

# Create a label to display the image
image_label = tk.Label(window, image=image)
image_label.pack()

# title label
title_label = tk.Label(text="Enter your title")
title_label.pack()

enter_title = tk.Entry()
enter_title.pack()

# secret message label
secret_label = tk.Label(text="Enter your secret")
secret_label.pack()

enter_secret = tk.Text(height=10, width=30)
enter_secret.pack()

# master key label
master_key_label = tk.Label(text="Enter master key")
master_key_label.pack()

enter_master_key = tk.Entry()
enter_master_key.pack()

encrypt_button = tk.Button(text="Save and encrypt", command=save_to_file)
encrypt_button.pack()
decrypt_button = tk.Button(text="Decrypt", command=decrypt_file)
decrypt_button.pack()

# Start the Tkinter event loop
window.mainloop()