import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3

# Create a connection to SQLite database
connection = sqlite3.connect("gym.db")  # Your database file name
cursor = connection.cursor()

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
connection.commit()

class EmployeePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Page")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Search field for employees
        self.search_var = tk.StringVar()
        tk.Label(root, text="Search Employee (Name or Code):", bg="white", fg="blue").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(root, textvariable=self.search_var).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Button(root, text="Search", command=self.search_employee, bg="blue", fg="white").grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Employee table
        self.tree = ttk.Treeview(root, columns=("name", "age", "photo", "start_date", "end_date", "job_title", "code"), show='headings')
        self.tree.heading("name", text="Name")
        self.tree.heading("age", text="Age")
        self.tree.heading("photo", text="Photo")
        self.tree.heading("start_date", text="Start Date")
        self.tree.heading("end_date", text="End Date")
        self.tree.heading("job_title", text="Job Title")
        self.tree.heading("code", text="Code")
        self.tree.column("name", width=150)
        self.tree.column("age", width=50)
        self.tree.column("photo", width=100)
        self.tree.column("start_date", width=120)
        self.tree.column("end_date", width=120)
        self.tree.column("job_title", width=150)
        self.tree.column("code", width=50)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Populate table with data from the database
        self.populate_table()

        # Add new employee button
        tk.Button(root, text="Add New Employee", command=self.add_new_employee, bg="blue", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Delete all data button
        tk.Button(root, text="Delete All Employees", command=self.delete_all_employees, bg="red", fg="white").grid(row=2, column=2, padx=10, pady=10, sticky="w")

    def populate_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor.execute("SELECT * FROM employee")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row[1],  # Name
                row[2],  # Age
                row[3] if row[3] else "N/A",  # Photo
                row[4],  # Start Date
                row[5],  # End Date
                row[6],  # Job Title
                row[0]   # Code
            ))

    def search_employee(self):
        search_term = self.search_var.get().lower()
        self.search_var.set("")  # Clear the search field
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor.execute("SELECT * FROM employee WHERE LOWER(name) LIKE ? OR CAST(code AS TEXT) LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
        results = cursor.fetchall()
        if results:
            for row in results:
                self.tree.insert("", "end", values=(row[1], row[2], row[3] if row[3] else "N/A", row[4], row[5], row[6], row[0]))
        else:
            messagebox.showerror("Error", "Employee not found")

    def add_new_employee(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Employee")
        add_window.configure(bg="white")

        # Name
        tk.Label(add_window, text="Name:", bg="white", fg="blue").grid(row=0, column=0, padx=10, pady=10)
        name_var = tk.StringVar()
        tk.Entry(add_window, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)

        # Age
        tk.Label(add_window, text="Age:", bg="white", fg="blue").grid(row=1, column=0, padx=10, pady=10)
        age_var = tk.IntVar()
        tk.Entry(add_window, textvariable=age_var).grid(row=1, column=1, padx=10, pady=10)

        # Photo
        tk.Label(add_window, text="Photo (URL/Path):", bg="white", fg="blue").grid(row=2, column=0, padx=10, pady=10)
        photo_var = tk.StringVar()
        tk.Entry(add_window, textvariable=photo_var).grid(row=2, column=1, padx=10, pady=10)

        # Start Date
        tk.Label(add_window, text="Start Date:", bg="white", fg="blue").grid(row=3, column=0, padx=10, pady=10)
        start_date_var = tk.StringVar()
        start_date_entry = DateEntry(add_window, textvariable=start_date_var, date_pattern='yyyy-mm-dd')
        start_date_entry.grid(row=3, column=1, padx=10, pady=10)

        # End Date
        tk.Label(add_window, text="End Date:", bg="white", fg="blue").grid(row=4, column=0, padx=10, pady=10)
        end_date_var = tk.StringVar()
        end_date_entry = DateEntry(add_window, textvariable=end_date_var, date_pattern='yyyy-mm-dd')
        end_date_entry.grid(row=4, column=1, padx=10, pady=10)

        # Job Title
        tk.Label(add_window, text="Job Title:", bg="white", fg="blue").grid(row=5, column=0, padx=10, pady=10)
        job_title_var = tk.StringVar(value="صيانه")
        job_title_combobox = ttk.Combobox(add_window, textvariable=job_title_var, values=["صيانه", "عامل نظافه", "باريستا", "علاج طبيعي"])
        job_title_combobox.grid(row=5, column=1, padx=10, pady=10)

        tk.Button(add_window, text="Save", command=lambda: self.save_employee(name_var, age_var, photo_var, start_date_var, end_date_var, job_title_var, add_window), bg="blue", fg="white").grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def save_employee(self, name_var, age_var, photo_var, start_date_var, end_date_var, job_title_var, window):
        try:
            name = name_var.get()
            age = age_var.get()
            photo = photo_var.get()
            start_date = start_date_var.get()
            end_date = end_date_var.get()
            job_title = job_title_var.get()

            if not name or not start_date or not end_date or not job_title:
                raise ValueError("All fields except photo are required.")

            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')

            cursor.execute("""
                INSERT INTO employee (name, age, photo, start_date, end_date, job_title)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, age, photo, start_date, end_date, job_title))

            connection.commit()
            window.destroy()
            self.refresh_table()
            messagebox.showinfo("Success", "Employee added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save employee: {e}")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_table()

    def delete_all_employees(self):
        cursor.execute("DELETE FROM employee")
        connection.commit()
        self.refresh_table()

# Main window setup
if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeePage(root)
    root.mainloop()

    # Close the connection when the program ends
    connection.close()
