import tkinter as tk

# Create the main window
window = tk.Tk()
window.config(padx=5, pady=5)
window.title("Image in Tkinter")
window.geometry("300x500")

# Load the image
image = tk.PhotoImage(file="topsecret.png")
image = image.subsample(6,6)

# Create a label to display the image
image_label = tk.Label(window, image=image)
image_label.pack()

# title label
title_label = tk.Label(text="Enter your title")
title_label.pack()

enter_title = tk.Entry()
enter_title.pack()

title = enter_title.get()

# secret message label
secret_label = tk.Label(text="Enter your secret")
secret_label.pack()

enter_secret = tk.Text(height=10, width=30)
enter_secret.pack()

secret_text = enter_secret.get(1.0, tk.END)

# master key label
master_key_label = tk.Label(text="Enter master key")
master_key_label.pack()

enter_master_key = tk.Entry()
enter_master_key.pack()

master_key = enter_master_key.get()

encrypt_button = tk.Button(text="Save and encrypt")
encrypt_button.pack()
decrypt_button = tk.Button(text="Decrypt")
decrypt_button.pack()


# Start the Tkinter event loop
window.mainloop()