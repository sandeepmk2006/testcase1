import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from threading import Thread

class HabitTrackerApp:
    def __init__(self, user, db_manager):
        self.user = user
        self.db_manager = db_manager
        self.habits = []
        self.current_habit_logs = {}
        self.current_month = datetime.now()
        self.root = tk.Tk()
        self.root.title(f"Habit Tracker - {user.name}")
        self.root.geometry("900x650")
        self.create_widgets()

    def create_widgets(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="x")
        self.user_label = tk.Label(self.top_frame, text=f"User: {self.user.name} (@{self.user.username})", font=("Arial", 12, "bold"), fg="#006400")
        self.user_label.pack(side="left")
        self.habit_label = tk.Label(self.top_frame, text="Select Habit:")
        self.habit_label.pack(side="left")
        self.habit_combo = ttk.Combobox(self.top_frame)
        self.habit_combo.pack(side="left")
        self.new_habit_button = tk.Button(self.top_frame, text="New Habit", command=self.create_new_habit)
        self.new_habit_button.pack(side="left")
        self.prev_month_button = tk.Button(self.top_frame, text="< Prev Month", command=lambda: self.change_month(-1))
        self.prev_month_button.pack(side="left")
        self.next_month_button = tk.Button(self.top_frame, text="Next Month >", command=lambda: self.change_month(1))
        self.next_month_button.pack(side="left")
        self.logout_button = tk.Button(self.top_frame, text="Logout", command=self.logout)
        self.logout_button.pack(side="left")

        self.center_frame = tk.Frame(self.root)
        self.center_frame.pack(fill="both", expand=True)
        self.header_frame = tk.Frame(self.center_frame)
        self.header_frame.pack(fill="x")
        self.year_label = tk.Label(self.header_frame, text=str(self.current_month.year), font=("Arial", 24, "bold"))
        self.year_label.pack(fill="x")
        self.month_label = tk.Label(self.header_frame, text=self.current_month.strftime("%B"), font=("Arial", 18, "bold"))
        self.month_label.pack(fill="x")
        self.calendar_frame = tk.Frame(self.center_frame)
        self.calendar_frame.pack(fill="both", expand=True)
        self.calendar_buttons = []
        for i in range(42):
            button = tk.Button(self.calendar_frame, text="", width=10, height=5, command=lambda i=i: self.on_day_clicked(i))
            button.grid(row=i // 7, column=i % 7)
            self.calendar_buttons.append(button)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill="x")
        self.streak_label = tk.Label(self.bottom_frame, text="Current Streak: 0 days", font=("Arial", 14, "bold"))
        self.streak_label.pack(side="left")
        self.export_button = tk.Button(self.bottom_frame, text="Export Report", command=self.export_report)
        self.export_button.pack(side="left")

        self.load_habits()

    def load_habits(self):
        self.habits = self.db_manager.get_habits_for_user(self.user.id)
        self.habit_combo['values'] = [habit.name for habit in self.habits]
        if self.habits:
            self.habit_combo.set(self.habits[0].name)
            self.on_habit_selected()

    def on_habit_selected(self):
        habit_name = self.habit_combo.get()
        for habit in self.habits:
            if habit.name == habit_name:
                self.current_habit_logs = self.db_manager.get_logs_for_habit(habit.id)
                self.update_calendar()
                self.update_streak()
                break

    def update_calendar(self):
        first_of_month = self.current_month.replace(day=1)
        days_in_month = self.current_month.month
        if self.current_month.month == 12:
            days_in_month = 31
        else:
            if self.current_month.year % 4 == 0 and (self.current_month.year % 100 != 0 or self.current_month.year % 400 == 0):
                if self.current_month.month == 2:
                    days_in_month = 29
            else:
                if self.current_month.month == 2:
                    days_in_month = 28
                elif self.current_month.month in [1, 3, 5, 7, 8, 10, 12]:
                    days_in_month = 31
                else:
                    days_in_month = 30
        first_day_of_week = first_of_month.weekday()
        today = datetime.now()
        self.year_label['text'] = str(self.current_month.year)
        self.month_label['text'] = self.current_month.strftime("%B")
        for i in range(42):
            self.calendar_buttons[i]['text'] = ""
            self.calendar_buttons[i]['bg'] = "#C0C0C0"
            self.calendar_buttons[i]['state'] = "disabled"
        for day in range(1, days_in_month + 1):
            button_index = first_day_of_week + day - 1
            if button_index < 42:
                self.calendar_buttons[button_index]['text'] = str(day)
                date = self.current_month.replace(day=day)
                if date < today:
                    self.calendar_buttons[button_index]['state'] = "disabled"
                    self.calendar_buttons[button_index]['tooltip'] = "Past dates cannot be edited"
                else:
                    self.calendar_buttons[button_index]['state'] = "normal"
                    self.calendar_buttons[button_index]['tooltip'] = "Click to toggle completion"
                if date in self.current_habit_logs:
                    if self.current_habit_logs[date]:
                        self.calendar_buttons[button_index]['bg'] = "#22C55E"
                    else:
                        self.calendar_buttons[button_index]['bg'] = "#EF4444"
                else:
                    if date < today:
                        self.calendar_buttons[button_index]['bg'] = "#C0C0C0"
                    else:
                        self.calendar_buttons[button_index]['bg'] = "#FFFFFF"

    def on_day_clicked(self, button_index):
        habit_name = self.habit_combo.get()
        if not habit_name:
            messagebox.showerror("Error", "Please select a habit first!")
            return
        day_text = self.calendar_buttons[button_index]['text']
        if not day_text:
            return
        day = int(day_text)
        date = self.current_month.replace(day=day)
        current_color = self.calendar_buttons[button_index]['bg']
        if current_color == "#FFFFFF":
            self.db_manager.log_habit(self.habits[self.habit_combo.current()]['id'], date, True)
            self.current_habit_logs[date] = True
            self.calendar_buttons[button_index]['bg'] = "#22C55E"
        elif current_color == "#22C55E":
            self.db_manager.log_habit(self.habits[self.habit_combo.current()]['id'], date, False)
            self.current_habit_logs[date] = False
            self.calendar_buttons[button_index]['bg'] = "#EF4444"
        elif current_color == "#EF4444":
            self.db_manager.delete_habit_log(self.habits[self.habit_combo.current()]['id'], date)
            del self.current_habit_logs[date]
            self.calendar_buttons[button_index]['bg'] = "#FFFFFF"
        self.update_streak()

    def create_new_habit(self):
        habit_name = messagebox.askstring("New Habit", "Enter habit name:")
        if habit_name:
            habit_id = self.db_manager.add_habit_for_user(habit_name, self.user.id)
            if habit_id:
                messagebox.showinfo("Success", "Habit created successfully!")
                self.load_habits()
            else:
                messagebox.showerror("Error", "Error creating habit!")

    def logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()

    def change_month(self, offset):
        if offset == -1:
            if self.current_month.month == 1:
                self.current_month = self.current_month.replace(year=self.current_month.year - 1, month=12)
            else:
                self.current_month = self.current_month.replace(month=self.current_month.month - 1)
        else:
            if self.current_month.month == 12:
                self.current_month = self.current_month.replace(year=self.current_month.year + 1, month=1)
            else:
                self.current_month = self.current_month.replace(month=self.current_month.month + 1)
        self.update_calendar()

    def update_streak(self):
        streak = 0
        today = datetime.now()
        today_status = self.current_habit_logs.get(today)
        if today_status is None or not today_status:
            self.streak_label['text'] = "Current Streak: 0 days"
            return
        check_date = today
        while check_date in self.current_habit_logs and self.current_habit_logs[check_date]:
            streak += 1
            check_date -= timedelta(days=1)
        self.streak_label['text'] = f"Current Streak: {streak} days"

    def export_report(self):
        habit_name = self.habit_combo.get()
        if not habit_name:
            messagebox.showerror("Error", "Please select a habit first!")
            return
        thread = Thread(target=self.export_report_thread, args=(habit_name,))
        thread.start()

    def export_report_thread(self, habit_name):
        try:
            with open("habit_report.txt", "w") as f:
                for date, status in self.current_habit_logs.items():
                    f.write(f"{date.strftime('%Y-%m-%d')}: {status}\n")
            messagebox.showinfo("Export Success", "Report exported successfully to habit_report.txt!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting report: {e}")

    def run(self):
        self.root.mainloop()

class User:
    def __init__(self, id, name, username):
        self.id = id
        self.name = name
        self.username = username

class DatabaseManager:
    def __init__(self):
        pass

    def get_habits_for_user(self, user_id):
        return []

    def get_logs_for_habit(self, habit_id):
        return {}

    def log_habit(self, habit_id, date, status):
        pass

    def delete_habit_log(self, habit_id, date):
        pass

    def add_habit_for_user(self, habit_name, user_id):
        return 0

class Habit:
    def __init__(self, id, name):
        self.id = id
        self.name = name

if __name__ == "__main__":
    db_manager = DatabaseManager()
    user = User(1, "John Doe", "johndoe")
    app = HabitTrackerApp(user, db_manager)
    app.run()