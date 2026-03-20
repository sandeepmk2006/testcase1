import os
import hashlib
import datetime
import mysql.connector
from mysql.connector import errorcode

class DatabaseManager:
    def __init__(self):
        self.url = None
        self.user = None
        self.password = None
        self.load_configuration()

    def load_configuration(self):
        try:
            with open("config.properties", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("db.url"):
                        self.url = line.split("=")[1].strip()
                    elif line.startswith("db.user"):
                        self.user = line.split("=")[1].strip()
                    elif line.startswith("db.password"):
                        self.password = line.split("=")[1].strip()
            print("Database configuration loaded successfully.")
        except FileNotFoundError:
            print("Error loading config.properties: File not found.")
            self.url = "jdbc:mysql://localhost:3306/habits"
            self.user = "root"
            self.password = ""

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_connection(self):
        try:
            cnx = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.url.split(":")[2].split("/")[0],
                database=self.url.split(":")[2].split("/")[2]
            )
            return cnx
        except mysql.connector.Error as err:
            print("Database connection error: {}".format(err))
            return None

    def log_habit(self, habit_id, date, completed):
        cnx = self.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = "SELECT id FROM habit_logs WHERE habit_id = %s AND date = %s"
            cursor.execute(query, (habit_id, date))
            result = cursor.fetchone()
            if result:
                log_id = result[0]
                query = "UPDATE habit_logs SET completed = %s WHERE id = %s"
                cursor.execute(query, (completed, log_id))
            else:
                query = "INSERT INTO habit_logs (habit_id, date, completed) VALUES (%s, %s, %s)"
                cursor.execute(query, (habit_id, date, completed))
            cnx.commit()
            cursor.close()
            cnx.close()

    def delete_habit_log(self, habit_id, date):
        cnx = self.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = "DELETE FROM habit_logs WHERE habit_id = %s AND date = %s"
            cursor.execute(query, (habit_id, date))
            cnx.commit()
            cursor.close()
            cnx.close()

    def get_logs_for_habit(self, habit_id):
        cnx = self.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = "SELECT date, completed FROM habit_logs WHERE habit_id = %s"
            cursor.execute(query, (habit_id,))
            result = cursor.fetchall()
            logs = {}
            for row in result:
                logs[row[0]] = row[1]
            cursor.close()
            cnx.close()
            return logs

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, name, username, email, password):
        cnx = self.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                print("Username already exists!")
                return -1
            query = "INSERT INTO users (name, username, email, password_hash) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, username, email, self.hash_password(password)))
            user_id = cursor.lastrowid
            cnx.commit()
            cursor.close()
            cnx.close()
            return user_id

    def login_user(self, username, password):
        cnx = self.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = "SELECT id, name, username, email, password_hash FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                stored_hash = result[4]
                input_hash = self.hash_password(password)
                if stored_hash == input_hash:
                    user = {
                        "id": result[0],
                        "name": result[1],
                        "username": result[2],
                        "email": result[3]
                    }
                    print("Login successful for user: {}".format(username))
                    return user
                else:
                    print("Invalid password!")
            else:
                print("User not found!")
            cursor.close()
            cnx.close()
            return None

    def add_habit_for_user(self, habit_name, user_id):
        cnx = self.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = "INSERT INTO habits (name, user_id) VALUES (%s, %s)"
            cursor.execute(query, (habit_name, user_id))
            habit_id = cursor.lastrowid
            cnx.commit()
            cursor.close()
            cnx.close()
            return habit_id

    def get_habits_for_user(self, user_id):
        cnx = self.get_connection()
        if cnx is not None:
            cursor = cnx.cursor()
            query = "SELECT id, name FROM habits WHERE user_id = %s ORDER BY name"
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
            habits = []
            for row in result:
                habits.append({
                    "id": row[0],
                    "name": row[1]
                })
            cursor.close()
            cnx.close()
            return habits

class User:
    def __init__(self, id, name, username, email):
        self.id = id
        self.name = name
        self.username = username
        self.email = email

class Habit:
    def __init__(self, id, name):
        self.id = id
        self.name = name