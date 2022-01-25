from tkinter import messagebox
import tkinter as tk
import string
import random


class Application(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Manager")
        self.window.config(padx=100, pady=100)

        self.logo = tk.PhotoImage(file="res/images/logo.png")
        self.canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
        self.canvas.create_image(100, 100, image=self.logo)
        self.canvas.grid(column=1, row=0)

        self.website_label = tk.Label(text="Website:", font=("Arial", 11))
        self.website_label.config(padx=25, pady=5)
        self.website_label.grid(column=0, row=1)

        self.username_label = tk.Label(text="Email/Username:", font=("Arial", 11))
        self.username_label.config(padx=25, pady=5)
        self.username_label.grid(column=0, row=2)

        self.password_label = tk.Label(text="Password:", font=("Arial", 11))
        self.password_label.config(padx=25, pady=5)
        self.password_label.grid(column=0, row=3)

        self.website_entry = tk.Entry(width=41, font=("Arial", 11))
        self.website_entry.grid(column=1, row=1, columnspan=2)
        self.website_entry.focus()

        self.username_entry = tk.Entry(width=41, font=("Arial", 11))
        self.username_entry.grid(column=1, row=2, columnspan=2)

        self.password_entry = tk.Entry(width=30, font=("Arial", 11))
        self.password_entry.grid(column=1, row=3)

        self.generate_pass_button = tk.Button(width=8, text="Generate", command=self.generate_password, font=("Arial", 11))
        self.generate_pass_button.grid(column=2, row=3)

        self.add_button = tk.Button(width=36, text="Add", command=self.add_password, font=("Arial", 11))
        self.add_button.grid(column=1, row=4, columnspan=2)

        self.get_button = tk.Button(width=36, text="Get", command=self.get_password, font=("Arial", 11))
        self.get_button.grid(column=1, row=5, columnspan=2)

        self.window.mainloop()

    def generate_password(self):
        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_"
        password = ""

        for _ in range(20):
            password += random.choice(characters)

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def get_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = None

        if "" in [website, username]:
            messagebox.showerror(title="Password Management System", message="Don't leave any of the fields empty! You need to provide a website and a username/email to fetch the password.")
            return

        with open("data/passwords.txt", "r") as f:
            for line in f.readlines():
                info = line.strip("\n").split(" | ")
                if info[0] == website and info[1] == username:
                    password = info[2]

        if password:
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            self.window.clipboard_clear()
            self.window.clipboard_append(password)
        else:
            # Popup for password not found
            messagebox.showerror(title="Password Management System", message=f"No password added for [{username}] on [{website}]")

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if "" in [website, username, password]:
            messagebox.showerror(title="Password Management System", message="Don't leave any of the fields empty!")
            return

        if not messagebox.askokcancel(title="Password Management System", message=f"These are the details entered:\nWebsite: {website}\nUsername/Email: {username}\nPassword: {password}\nIs it OK to save?"):
            return

        self.website_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        pass_set = False
        new_passwords = []

        with open("data/passwords.txt", "r") as f:
            passwords = f.read().strip("\n").split("\n")

        for existing_password in passwords:
            if existing_password == "":
                continue
            info = existing_password.split(" | ")
            if info[0] == website and info[1] == username:
                info[2] = password
                pass_set = True
            new_passwords.append(" | ".join(info))

        if not pass_set:
            new_passwords.append(f"{website} | {username} | {password}")

        with open("data/passwords.txt", "w") as f:
            f.write("\n".join(new_passwords))

        self.window.clipboard_clear()
        self.window.clipboard_append(password)
