# Tkinter Account Manager

A simple desktop-based User Account Management System built with Python and Tkinter. This application allows users to register, log in, and manage their profiles using a graphical interface. User data is stored securely in a local JSON file.

## Features

- ✅ User registration with unique usernames
- 🔐 Login authentication with password validation
- 🧑 View and update account information
- 💾 Persistent storage using `accounts.json`
- 🎨 Styled GUI with Tkinter for an improved user experience

## Requirements

- Python 3.8+
- No external libraries required (only built-in modules)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tkinter-account-manager.git
   cd tkinter-account-manager

2.   Run the app
   python main.py

File Structure
tkinter-account-manager/
├── main.py               # Main Tkinter GUI logic
├── user_account.py       # User account class and methods
├── accounts.json         # Stores registered user data
├── README.md             # Project documentation

3. Future Improvements
  Add password hashing for better security
  Improve UI with more styles/themes
  Add password reset functionality
  Connect to a real database (e.g., SQLite or Firebase)
  
