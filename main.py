import json
import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, StringVar, BooleanVar

ACCOUNTS_FILE = 'accounts.json'
current_theme = "flatly"

def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as f:
        json.dump(accounts, f, indent=4)

def register_window():
    reg_win = tb.Toplevel()
    reg_win.transient(root)
    reg_win.grab_set()
    reg_win.title("Create Account")
    reg_win.geometry("500x300")
    reg_win.resizable(True, True)

    frame = tb.Frame(reg_win, padding=30)
    frame.pack(fill=BOTH, expand=True)
    frame.columnconfigure(1, weight=1)

    tb.Label(frame, text="Register", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tb.Label(frame, text="Username:").grid(row=1, column=0, sticky="e", padx=(0, 10))
    username_entry = tb.Entry(frame, width=30)
    username_entry.grid(row=1, column=1, sticky="ew")

    tb.Label(frame, text="Email:").grid(row=2, column=0, sticky="e", padx=(0, 10))
    email_entry = tb.Entry(frame, width=30)
    email_entry.grid(row=2, column=1, sticky="ew")

    tb.Label(frame, text="Password:").grid(row=3, column=0, sticky="e", padx=(0, 10))
    password_entry = tb.Entry(frame, show="*", width=30)
    password_entry.grid(row=3, column=1, sticky="ew")

    tb.Label(frame, text="Confirm Password:").grid(row=4, column=0, sticky="e", padx=(0, 10))
    confirm_entry = tb.Entry(frame, show="*", width=30)
    confirm_entry.grid(row=4, column=1, sticky="ew")

    def register():
        username = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        confirm = confirm_entry.get().strip()

        if not username or not email or not password or not confirm:
            messagebox.showwarning("Missing Fields", "Please fill out all fields.")
            return
        if password != confirm:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return
        accounts = load_accounts()
        if any(a['email'] == email for a in accounts):
            messagebox.showerror("Exists", "Email already registered.")
            return
        accounts.append({"username": username, "email": email, "password": password})
        save_accounts(accounts)
        messagebox.showinfo("Success", "Account created!")
        reg_win.destroy()

    tb.Button(frame, text="Register", command=register, bootstyle="success-outline").grid(row=5, column=0, columnspan=2, pady=20)

def main_app(username):
    def build_window():
        def logout():
            main_win.destroy()
            launch_login_window()

        main_win = tb.Window(themename=current_theme)
        main_win.title("Dashboard")
        main_win.geometry("800x500")
        main_win.resizable(True, True)

        frame = tb.Frame(main_win, padding=30)
        frame.pack(fill=BOTH, expand=True)

        tb.Label(frame, text=f"Welcome, {username}", font=("Segoe UI", 18)).pack(pady=10)

        tree = tb.Treeview(frame, columns=("Username", "Email"), show="headings", bootstyle="info")
        tree.heading("Username", text="Username")
        tree.heading("Email", text="Email")
        tree.pack(fill=BOTH, expand=True, pady=10)

        def refresh_tree():
            tree.delete(*tree.get_children())
            for acc in load_accounts():
                tree.insert("", END, values=(acc["username"], acc["email"]))

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No selection", "Please select a user to delete.")
                return
            item = tree.item(selected[0])
            email_to_delete = item['values'][1]
            accounts = load_accounts()
            accounts = [a for a in accounts if a["email"] != email_to_delete]
            save_accounts(accounts)
            refresh_tree()

        def add_account_popup():
            popup = tb.Toplevel(themename=current_theme)
            popup.title("Add User")
            popup.geometry("400x250")
            popup.resizable(False, False)
            pf = tb.Frame(popup, padding=20)
            pf.pack(fill=BOTH, expand=True)
            pf.columnconfigure(1, weight=1)

            tb.Label(pf, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
            uname = tb.Entry(pf)
            uname.grid(row=0, column=1, pady=5)

            tb.Label(pf, text="Email:").grid(row=1, column=0, sticky="e", pady=5)
            uemail = tb.Entry(pf)
            uemail.grid(row=1, column=1, pady=5)

            tb.Label(pf, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
            upass = tb.Entry(pf, show="*")
            upass.grid(row=2, column=1, pady=5)

            def add_user():
                username, email, password = uname.get(), uemail.get(), upass.get()
                if not username or not email or not password:
                    messagebox.showerror("Missing", "All fields are required.")
                    return
                accounts = load_accounts()
                if any(a['email'] == email for a in accounts):
                    messagebox.showerror("Exists", "User already exists.")
                    return
                accounts.append({"username": username, "email": email, "password": password})
                save_accounts(accounts)
                popup.destroy()
                refresh_tree()

            tb.Button(pf, text="Add", command=add_user, bootstyle="success-outline").grid(row=3, column=0, columnspan=2, pady=15)

        btns = tb.Frame(frame)
        btns.pack(pady=10, anchor='center')
        tb.Button(btns, text="Add User", command=add_account_popup, bootstyle="success").pack(side="left", padx=5)
        tb.Button(btns, text="Delete Selected", command=delete_selected, bootstyle="danger").pack(side="left", padx=5)
        tb.Button(frame, text="Logout", command=logout, bootstyle="info-outline").pack(pady=10)

        refresh_tree()
        main_win.mainloop()

    build_window()

def launch_login_window():
    global root
    root = tb.Window(themename=current_theme)
    root.title("Login")
    root.geometry("500x250")
    root.minsize(400, 200)
    root.resizable(True, True)

    frame = tb.Frame(root, padding=30)
    frame.pack(fill=BOTH, expand=True)
    frame.columnconfigure(1, weight=1)

    tb.Label(frame, text="User Login", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

    tb.Label(frame, text="Email:").grid(row=1, column=0, sticky="e", padx=(0, 10))
    email_entry = tb.Entry(frame, width=30)
    email_entry.grid(row=1, column=1, sticky="ew")

    tb.Label(frame, text="Password:").grid(row=2, column=0, sticky="e", padx=(0, 10), pady=(10, 0))
    password_var = StringVar()
    password_entry = tb.Entry(frame, textvariable=password_var, show="*", width=30)
    password_entry.grid(row=2, column=1, sticky="ew", pady=(10, 0))

    def toggle_password():
        password_entry.config(show="" if show_pass.get() else "*")

    show_pass = BooleanVar()
    tb.Checkbutton(frame, text="Show Password", variable=show_pass, command=toggle_password).grid(row=3, column=1, sticky="w", pady=5)

    def try_login():
        email = email_entry.get().strip()
        password = password_var.get().strip()
        accounts = load_accounts()
        for acc in accounts:
            if acc['email'] == email and acc['password'] == password:
                root.destroy()
                main_app(acc['username'])
                return
        messagebox.showerror("Failed", "Invalid credentials.")

    btn_frame = tb.Frame(frame)
    btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

    tb.Button(btn_frame, text="Login", command=try_login, bootstyle="primary").pack(side="left", padx=5)
    tb.Button(btn_frame, text="Create Account", command=register_window, bootstyle="secondary").pack(side="left", padx=5)

    root.mainloop()
    return None

if __name__ == "__main__":
    while True:
        root = launch_login_window()
        if root is None:
            break