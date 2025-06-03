import tkinter as tk
from tkinter import messagebox, Listbox, END
import json
import os

DATA_FILE = 'accounts.json'


def load_accounts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []


def save_accounts(accounts):
    with open(DATA_FILE, 'w') as f:
        json.dump(accounts, f, indent=4)


def refresh_account_list():
    account_list.delete(0, END)
    for i, acc in enumerate(accounts):
        account_list.insert(END, f"{i + 1}. {acc['username']} - {acc['email']}")


def add_account():
    username = username_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not email or not password:
        messagebox.showwarning("Missing Fields", "Please fill out all fields.")
        return

    accounts.append({'username': username, 'email': email, 'password': password})
    save_accounts(accounts)
    refresh_account_list()
    username_entry.delete(0, END)
    email_entry.delete(0, END)
    password_entry.delete(0, END)


def delete_selected():
    selected = account_list.curselection()
    if not selected:
        messagebox.showinfo("Select Account", "Please select an account to delete.")
        return

    index = selected[0]
    del accounts[index]
    save_accounts(accounts)
    refresh_account_list()


# Load existing data
accounts = load_accounts()

# GUI setup
root = tk.Tk()
root.title("User Account Manager")
root.geometry("500x450")

tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root, width=40)
username_entry.pack()

tk.Label(root, text="Email:").pack(pady=5)
email_entry = tk.Entry(root, width=40)
email_entry.pack()

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*", width=40)
password_entry.pack()

tk.Button(root, text="Add Account", width=20, command=add_account).pack(pady=10)

account_list = Listbox(root, width=60, height=10)
account_list.pack(pady=10)

tk.Button(root, text="Delete Selected", width=20, command=delete_selected).pack(pady=5)

refresh_account_list()
root.mainloop()