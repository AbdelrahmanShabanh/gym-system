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
    start_date TEXT NOT NULL DEFAULT (strftime('%d/%m/%Y', 'now')),
    experience_year INTEGER,
    end_date TEXT,
    specialization TEXT DEFAULT 'body building',
    CHECK (specialization IN ('cross fit', 'body building', 'workout')) 
)
""")
connection.commit()


class TrainersPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Trainers Page")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Search field for trainers
        self.search_var = tk.StringVar()
        tk.Label(root, text="Search Trainer (Name or Code):", bg="white", fg="blue").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(root, textvariable=self.search_var).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Button(root, text="Search", command=self.search_trainer, bg="blue", fg="white").grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Trainer table
        self.tree = ttk.Treeview(root, columns=("name", "age", "gender", "start_date", "end_date", "experience_year", "specialization", "code"), show='headings')
        self.tree.heading("name", text="Name")
        self.tree.heading("age", text="Age")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("start_date", text="Start Date")
        self.tree.heading("end_date", text="End Date")
        self.tree.heading("experience_year", text="Experience (Years)")
        self.tree.heading("specialization", text="Specialization")
        self.tree.heading("code", text="Code")
        self.tree.column("name", width=100)
        self.tree.column("age", width=50)
        self.tree.column("gender", width=70)
        self.tree.column("start_date", width=120)
        self.tree.column("end_date", width=100)
        self.tree.column("experience_year", width=120)
        self.tree.column("specialization", width=120)
        self.tree.column("code", width=70)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Populate table with data from the database
        self.populate_table()

        # Add new trainer button
        tk.Button(root, text="Add New Trainer", command=self.add_new_trainer, bg="blue", fg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # Delete all data button
        tk.Button(root, text="Delete All Trainers", command=self.delete_all_trainers, bg="red", fg="white").grid(row=2, column=2, padx=10, pady=10, sticky="w")

    def populate_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor.execute("SELECT * FROM coaches")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(
                row[1],  # Name
                row[3],  # Age
                row[2],  # Gender
                row[4],  # Start Date
                row[5] if row[5] else "N/A",  # End Date
                row[6],  # Experience Years
                row[7],  # Specialization
                row[0]   # Code
            ))

    def search_trainer(self):
        search_term = self.search_var.get().lower()
        self.search_var.set("")  # Clear the search field
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor.execute("SELECT * FROM coaches WHERE LOWER(name) LIKE ? OR CAST(code AS TEXT) LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
        results = cursor.fetchall()
        if results:
            for row in results:
                self.tree.insert("", "end", values=(row[1], row[3], row[2], row[4], row[5] if row[5] else "N/A", row[6], row[7], row[0]))
        else:
            messagebox.showerror("Error", "Trainer not found")

    def add_new_trainer(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Trainer")
        add_window.configure(bg="white")

        # Name
        tk.Label(add_window, text="Name:", bg="white", fg="blue").grid(row=0, column=0, padx=10, pady=10)
        name_var = tk.StringVar()
        tk.Entry(add_window, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)

        # Age
        tk.Label(add_window, text="Age:", bg="white", fg="blue").grid(row=1, column=0, padx=10, pady=10)
        age_var = tk.IntVar()
        tk.Entry(add_window, textvariable=age_var).grid(row=1, column=1, padx=10, pady=10)

        # Gender
        tk.Label(add_window, text="Gender:", bg="white", fg="blue").grid(row=2, column=0, padx=10, pady=10)
        gender_var = tk.StringVar(value="Male")
        tk.Radiobutton(add_window, text="Male", variable=gender_var, value="Male", bg="white", fg="blue").grid(row=2, column=1, padx=10, pady=10)
        tk.Radiobutton(add_window, text="Female", variable=gender_var, value="Female", bg="white", fg="blue").grid(row=2, column=2, padx=10, pady=10)

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

        # Experience (Manually editable)
        tk.Label(add_window, text="Experience (Years):", bg="white", fg="blue").grid(row=5, column=0, padx=10, pady=10)
        experience_var = tk.StringVar()
        tk.Entry(add_window, textvariable=experience_var).grid(row=5, column=1, padx=10, pady=10)

        # Specialization
        tk.Label(add_window, text="Specialization:", bg="white", fg="blue").grid(row=6, column=0, padx=10, pady=10)
        specialization_var = tk.StringVar(value="body building")
        specialization_combobox = ttk.Combobox(add_window, textvariable=specialization_var, values=["cross fit", "body building", "workout"])
        specialization_combobox.grid(row=6, column=1, padx=10, pady=10)

        tk.Button(add_window, text="Save", command=lambda: self.save_trainer(name_var, age_var, gender_var, start_date_var, end_date_var, experience_var, specialization_var, add_window), bg="blue", fg="white").grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def save_trainer(self, name_var, age_var, gender_var, start_date_var, end_date_var, experience_var, specialization_var, window):
        try:
            name = name_var.get()
            age = age_var.get()
            gender = gender_var.get()
            start_date = start_date_var.get()
            end_date = end_date_var.get() if end_date_var.get() else None
            experience = experience_var.get()
            specialization = specialization_var.get()

            if not name or not gender or not start_date or not specialization:
                raise ValueError("Name, Gender, Start Date, and Specialization are required fields.")
            
            if not experience.isdigit():
                raise ValueError("Experience must be a valid number.")

            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')

            cursor.execute("""
                INSERT INTO coaches (name, age, gender, start_date, end_date, experience_year, specialization)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, age, gender, start_date, end_date, experience, specialization))

            connection.commit()
            window.destroy()
            self.refresh_table()
            messagebox.showinfo("Success", "Trainer added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save trainer: {e}")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_table()

    def delete_all_trainers(self):
        cursor.execute("DELETE FROM coaches")
        connection.commit()
        self.refresh_table()


# Main window setup
if __name__ == "__main__":
    root = tk.Tk()
    app = TrainersPage(root)
    root.mainloop()