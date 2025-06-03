import json
import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox  # FIXED: standard messagebox

DATA_FILE = 'accounts.json'

# ------------------- Data Handling ------------------- #
def load_accounts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_accounts(accounts):
    with open(DATA_FILE, 'w') as f:
        json.dump(accounts, f, indent=4)

accounts = load_accounts()

# ------------------- Dashboard Window ------------------- #
def show_main_app(current_user):
    def refresh_account_list():
        account_list.delete(*account_list.get_children())
        for i, acc in enumerate(accounts):
            account_list.insert("", "end", values=(i + 1, acc['username'], acc['email']))

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
        selected = account_list.selection()
        if not selected:
            messagebox.showinfo("Select Account", "Please select an account to delete.")
            return
        index = int(account_list.item(selected[0])['values'][0]) - 1
        del accounts[index]
        save_accounts(accounts)
        refresh_account_list()

    def view_profile():
        messagebox.showinfo("Profile", f"Username: {current_user['username']}\nEmail: {current_user['email']}")

    def logout():
        root.destroy()
        show_auth_window()

    root = tb.Window(themename="darkly")
    root.title("User Account Manager")
    root.geometry("650x520")
    root.resizable(False, False)

    header_frame = tb.Frame(root)
    header_frame.pack(pady=10)

    tb.Label(header_frame, text=f"Welcome, {current_user['username']}!", font=("Helvetica", 16, "bold")).pack(side=LEFT, padx=10)
    tb.Button(header_frame, text="View Profile", bootstyle="secondary", command=view_profile).pack(side=LEFT, padx=5)
    tb.Button(header_frame, text="Logout", bootstyle="danger", command=logout).pack(side=LEFT, padx=5)

    frame = tb.Frame(root)
    frame.pack()

    tb.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    username_entry = tb.Entry(frame, width=30)
    username_entry.grid(row=0, column=1, pady=5)

    tb.Label(frame, text="Email:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    email_entry = tb.Entry(frame, width=30)
    email_entry.grid(row=1, column=1, pady=5)

    tb.Label(frame, text="Password:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    password_entry = tb.Entry(frame, show="*", width=30)
    password_entry.grid(row=2, column=1, pady=5)

    tb.Button(frame, text="Add Account", bootstyle="success", width=25, command=add_account).grid(row=3, column=0, columnspan=2, pady=10)

    columns = ("#", "Username", "Email")
    account_list = tb.Treeview(root, columns=columns, show="headings", height=10, bootstyle="dark")
    for col in columns:
        account_list.heading(col, text=col)
        account_list.column(col, anchor="center")
    account_list.pack(pady=10)

    tb.Button(root, text="Delete Selected", bootstyle="danger", width=25, command=delete_selected).pack(pady=5)

    refresh_account_list()
    root.mainloop()

# ------------------- Login/Register Window ------------------- #
def show_auth_window():
    win = tb.Window(themename="darkly")
    win.title("Login / Register")
    win.geometry("400x300")
    win.resizable(False, False)

    tabs = tb.Notebook(win)
    login_tab = tb.Frame(tabs)
    register_tab = tb.Frame(tabs)

    tabs.add(login_tab, text="Login")
    tabs.add(register_tab, text="Register")
    tabs.pack(expand=1, fill="both")

    # --- Login Tab --- #
    tb.Label(login_tab, text="Email:").pack(pady=5)
    login_email = tb.Entry(login_tab, width=30)
    login_email.pack()

    tb.Label(login_tab, text="Password:").pack(pady=5)
    login_password = tb.Entry(login_tab, width=30, show="*")
    login_password.pack()

    def login_action():
        email = login_email.get().strip()
        password = login_password.get().strip()
        for user in accounts:
            if user['email'] == email and user['password'] == password:
                win.destroy()
                show_main_app(user)
                return
        messagebox.showerror("Login Failed", "Invalid email or password.")

    tb.Button(login_tab, text="Log In", bootstyle="primary", command=login_action).pack(pady=10)

    # --- Register Tab --- #
    tb.Label(register_tab, text="Username:").pack(pady=5)
    reg_username = tb.Entry(register_tab, width=30)
    reg_username.pack()

    tb.Label(register_tab, text="Email:").pack(pady=5)
    reg_email = tb.Entry(register_tab, width=30)
    reg_email.pack()

    tb.Label(register_tab, text="Password:").pack(pady=5)
    reg_password = tb.Entry(register_tab, width=30, show="*")
    reg_password.pack()

    def register_action():
        username = reg_username.get().strip()
        email = reg_email.get().strip()
        password = reg_password.get().strip()
        if not username or not email or not password:
            messagebox.showwarning("Missing Fields", "Please complete all fields.")
            return
        for user in accounts:
            if user['email'] == email:
                messagebox.showerror("Already Exists", "That email is already registered.")
                return
        accounts.append({'username': username, 'email': email, 'password': password})
        save_accounts(accounts)
        messagebox.showinfo("Registered", "Account created! You can now log in.")
        reg_username.delete(0, END)
        reg_email.delete(0, END)
        reg_password.delete(0, END)

    tb.Button(register_tab, text="Register", bootstyle="success", command=register_action).pack(pady=10)

    win.mainloop()

# ------------------- Start App ------------------- #
if __name__ == '__main__':
    show_auth_window()