import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("gym.db")
cursor = connection.cursor()

# Create the coaches table
cursor.execute("""
CREATE TABLE IF NOT EXISTS coaches (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NUll,
    age INTEGER,
    start_date TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now')),
    experience_year INTEGER,
    end_date TEXT,
    specialization TEXT DEFAULT 'body building',
    CHECK (specialization IN ('cross fit', 'body building', 'workout')) 
)
""")
# Create the employee table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    photo TEXT,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    job_title TEXT NOT NULL,
    CHECK (job_title IN ('صيانه', 'عامل نظافه', 'باريستا', 'علاج طبيعي'))
)
""")

# Create the salary table
cursor.execute("""
CREATE TABLE IF NOT EXISTS salary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coach_code INTEGER,
    employee_code INTEGER,
    salary REAL DEFAULT 0,
    FOREIGN KEY (coach_code) REFERENCES coaches (code),
    FOREIGN KEY (employee_code) REFERENCES employee (code)
)
""")
connection.commit()

class salariesPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Salaries Page")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
         # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Search field for trainers and employees
        self.search_var = tk.StringVar()
        tk.Label(root, text="Search (Name or Code):", bg="white", fg="blue").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(root, textvariable=self.search_var).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Button(root, text="Search", command=self.search, bg="blue", fg="white").grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Trainers & Employee table
        self.tree = ttk.Treeview(root, columns=("name", "job_title", "salary", "code"), show='headings')
        self.tree.heading("name", text="Name")
        self.tree.heading("job_title", text="Job Title")
        self.tree.heading("salary", text="Salary")
        self.tree.heading("code", text="Code")
        self.tree.column("name", width=150)
        self.tree.column("job_title", width=150)
        self.tree.column("salary", width=120)
        self.tree.column("code", width=50)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Populate table with data from the database
        self.populate_table()

    def calculate_salary(self, start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        days_between = (end_date - start_date).days
        salary = days_between * 200
        if days_between >= 30:
            salary = 6000
        return salary

    def add_salaries(self):
        cursor.execute("SELECT code, start_date, end_date FROM employee")
        employees = cursor.fetchall()
        for emp in employees:
            salary = self.calculate_salary(emp[1], emp[2])
            cursor.execute("INSERT INTO salary (employee_code, salary) VALUES (?, ?)", (emp[0], salary))

        cursor.execute("SELECT code, start_date, end_date FROM coaches")
        coaches = cursor.fetchall()
        for coach in coaches:
            salary = self.calculate_salary(coach[1], coach[2])
            cursor.execute("INSERT INTO salary (coach_code, salary) VALUES (?, ?)", (coach[0], salary))

        connection.commit()

    def populate_table(self):
        self.add_salaries()
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor.execute("""
            SELECT e.name, e.job_title, s.salary, e.code
            FROM employee e
            LEFT JOIN salary s ON e.code = s.employee_code
            UNION
            SELECT c.name, c.specialization, s.salary, c.code
            FROM coaches c
            LEFT JOIN salary s ON c.code = s.coach_code
        """)
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def search(self):
        search_term = self.search_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor.execute("""
            SELECT e.name, e.job_title, s.salary, e.code
            FROM employee e
            LEFT JOIN salary s ON e.code = s.employee_code
            WHERE e.name LIKE ? OR e.code LIKE ?
            UNION
            SELECT c.name, c.specialization, s.salary, c.code
            FROM coaches c
            LEFT JOIN salary s ON c.code = s.coach_code
            WHERE c.name LIKE ? OR c.code LIKE ?
        """, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

# Main window setup
if __name__ == "__main__":
    root = tk.Tk()
    app = salariesPage(root)
    root.mainloop()