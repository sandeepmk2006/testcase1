import tkinter as tk
from tkinter import messagebox

class DatabaseManager:
    def __init__(self):
        pass

    def login_user(self, username, password):
        # implement database logic to login a user
        pass

    def register_user(self, name, username, email, password):
        # implement database logic to register a user
        pass

class HabitTrackerApp:
    def __init__(self, user, db_manager):
        # implement the habit tracker application
        pass

class LoginFrame:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.logged_in_user = None
        self.root = tk.Tk()
        self.root.title("Habit Tracker - Login")
        self.root.geometry("400x300")
        self.root.config(padx=10, pady=10)

        self.tab_control = tk.Notebook(self.root)
        self.login_tab = tk.Frame(self.tab_control)
        self.register_tab = tk.Frame(self.tab_control)
        self.tab_control.add(self.login_tab, text="Login")
        self.tab_control.add(self.register_tab, text="Register")
        self.tab_control.pack(expand=1, fill="both")

        self.create_login_tab()
        self.create_register_tab()

        self.root.mainloop()

    def create_login_tab(self):
        login_frame = tk.Frame(self.login_tab)
        login_frame.pack(fill="both", expand=1)

        tk.Label(login_frame, text="Login to Habit Tracker", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(login_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        self.username_field = tk.Entry(login_frame)
        self.username_field.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(login_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.password_field = tk.Entry(login_frame, show="*")
        self.password_field.grid(row=2, column=1, padx=5, pady=5)

        login_button = tk.Button(login_frame, text="Login", command=self.handle_login)
        login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def create_register_tab(self):
        register_frame = tk.Frame(self.register_tab)
        register_frame.pack(fill="both", expand=1)

        tk.Label(register_frame, text="Create New Account", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(register_frame, text="Full Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_field = tk.Entry(register_frame)
        self.name_field.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(register_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_field = tk.Entry(register_frame)
        self.email_field.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(register_frame, text="Username:").grid(row=3, column=0, padx=5, pady=5)
        self.reg_username_field = tk.Entry(register_frame)
        self.reg_username_field.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(register_frame, text="Password:").grid(row=4, column=0, padx=5, pady=5)
        self.reg_password_field = tk.Entry(register_frame, show="*")
        self.reg_password_field.grid(row=4, column=1, padx=5, pady=5)

        register_button = tk.Button(register_frame, text="Create Account", command=self.handle_register)
        register_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def handle_login(self):
        username = self.username_field.get()
        password = self.password_field.get()

        if not username or not password:
            messagebox.showerror("Login Error", "Please enter both username and password!")
            return

        self.logged_in_user = self.db_manager.login_user(username, password)

        if self.logged_in_user:
            messagebox.showinfo("Login Successful", f"Welcome back, {self.logged_in_user}!")
            self.open_main_application()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
            self.password_field.delete(0, tk.END)

    def handle_register(self):
        name = self.name_field.get()
        email = self.email_field.get()
        username = self.reg_username_field.get()
        password = self.reg_password_field.get()

        if not name or not email or not username or not password:
            messagebox.showerror("Registration Error", "Please fill in all fields!")
            return

        if len(password) < 6:
            messagebox.showerror("Registration Error", "Password must be at least 6 characters long!")
            return

        user_id = self.db_manager.register_user(name, username, email, password)

        if user_id > 0:
            messagebox.showinfo("Registration Successful", "Account created successfully! Please login.")
            self.name_field.delete(0, tk.END)
            self.email_field.delete(0, tk.END)
        else:
            messagebox.showerror("Registration Error", "Registration failed! Username may already exist.")

    def open_main_application(self):
        self.root.destroy()
        HabitTrackerApp(self.logged_in_user, self.db_manager)

if __name__ == "__main__":
    LoginFrame()