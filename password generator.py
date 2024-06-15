import random
import string
import tkinter as tk
from tkinter import messagebox

def generate_password(length):
    if length < 4:
        raise ValueError("Password length should be of at least 4 characters.")

    
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation

   
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_chars)
    ]

    if length > 4:
        all_chars = lowercase + uppercase + digits + special_chars
        password.extend(random.choice(all_chars) for _ in range(length - 4))

    random.shuffle(password)

    return ''.join(password)

def on_generate_button_click():
    try:
        length = int(length_entry.get())
        password = generate_password(length)
        result_label.config(text=f"Generated Password: {password}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


app = tk.Tk()
app.title("Password Generator")
app.geometry("400x200")
app.config(bg="#282c34")


tk.Label(app, text="Enter the desired length for the password:", bg="#282c34", fg="white", font=("Helvetica", 12)).pack(pady=10)
length_entry = tk.Entry(app, font=("Helvetica", 12))
length_entry.pack(pady=5)

generate_button = tk.Button(app, text="Generate Password", command=on_generate_button_click, bg="#61afef", fg="white", font=("Helvetica", 12))
generate_button.pack(pady=10)

result_label = tk.Label(app, text="Generated Password: ", bg="#282c34", fg="#98c379", font=("Helvetica", 12))
result_label.pack(pady=10)


app.mainloop()
