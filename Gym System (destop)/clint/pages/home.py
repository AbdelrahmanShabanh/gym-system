import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from datetime import datetime
import sqlite3
from login_page_module import LoginPage
from next_login import launch_next_page
from employee import EmployeePage
from Trainers import TrainersPage
from Salaries import salariesPage

# Database connection setup
connection = sqlite3.connect("gym.db")
cursor = connection.cursor()

# Create the users table if it doesn't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    amount INTEGER NOT NULL,
    photo TEXT,
    age INTEGER,
    start_date TEXT NOT NULL DEFAULT (strftime('%d/%m/%Y', 'now')),
    end_date TEXT NOT NULL
)
""")
connection.commit()

if __name__ == "__main__":
    def create_gym_app(root):
        from home import GymApp  
        app = GymApp(root)

    # Create login window
    root = tk.Tk()
    root.title("Login Page")
    login_page = LoginPage(root, lambda: launch_next_page(create_gym_app))  # Pass the function to create GymApp
    root.mainloop()

class GymApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Go Gym")
        self.root.configure(bg="white")
        self.root.iconbitmap("Gym.ico")
        # Configure grid layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_columnconfigure(4, weight=1)
        self.root.grid_columnconfigure(5, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Search field
        self.search_var = tk.StringVar()
        tk.Label(root, text="Search Customer (Name or Code):", bg="white", fg="blue").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(root, textvariable=self.search_var).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Button(root, text="Search", command=self.search_customer, bg="blue", fg="white").grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # Customer table
        self.tree = ttk.Treeview(root, columns=("name", "age", "phone_number", "gender", "amount", "start_date", "end_date", "code"), show='headings')
        self.tree.heading("name", text="Name")
        self.tree.heading("age", text="Age")
        self.tree.heading("phone_number", text="Phone Number")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("start_date", text="Start Date")
        self.tree.heading("end_date", text="End Date")
        self.tree.heading("code", text="Code")
        self.tree.column("name", width=100)
        self.tree.column("age", width=50)
        self.tree.column("phone_number", width=100)
        self.tree.column("gender", width=70)
        self.tree.column("amount", width=70)
        self.tree.column("start_date", width=100)
        self.tree.column("end_date", width=100)
        self.tree.column("code", width=70)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Populate table with data from the database
        self.populate_table()

        # Load and display the gym logo
        logo_path = "gymbg.png"  
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((250, 250), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)
        tk.Label(root, image=logo_photo, bg="white").grid(row=1, column=3, columnspan=3, padx=0, pady=10)
        self.root.logo_photo = logo_photo  # Keep a reference to avoid garbage collection

        # Enter code field
        tk.Label(root, text="Enter Your Code:", bg="white", fg="blue").grid(row=2, column=2, padx=0, pady=10, sticky="w")
        self.code_var = tk.StringVar()
        tk.Entry(root, textvariable=self.code_var).grid(row=2, column=3, padx=10, pady=10, sticky="w")
        tk.Button(root, text="Enter", command=self.enter_code, bg="blue", fg="white").grid(row=2, column=4, padx=10, pady=10, sticky="w")

        # Add new member button
        tk.Button(root, text="Add New Member", command=self.add_new_member, bg="blue", fg="white").grid(row=3, column=3, padx=10, pady=10, sticky="w")

        # Delete all data button
        tk.Button(root, text="Delete All Data", command=self.delete_all_data, bg="red", fg="white").grid(row=3, column=4, padx=10, pady=10, sticky="w")

        # Create a style for the OptionMenu
        style = ttk.Style()
        style.configure('TMenubutton', background='blue', foreground='white') # tmenubutton is the default style for OptionMenu

        # Dropdown menu for navigation
        self.pages = ["Home", "Employee", "Trainers", "Salaries"]
        self.selected_page = tk.StringVar()
        self.selected_page.set(self.pages[0])  # Default value

        ttk.OptionMenu(root, self.selected_page, *self.pages, command=self.navigate_to_page).grid(row=3, column=0, padx=10, pady=10, sticky="w")

    def populate_table(self):
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(row[1], row[5], row[2], row[3], row[4], row[6], row[7], row[0]))

    def search_customer(self):
        search_term = self.search_var.get().lower()
        self.search_var.set("")  # Clear the search field
        found = False
        for item in self.tree.get_children():
            self.tree.delete(item)
        cursor.execute("SELECT * FROM users WHERE LOWER(name) LIKE ? OR code LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=(row[1], row[5], row[2], row[3], row[4], row[6], row[7], row[0]))
            found = True
        if not found:
            messagebox.showerror("Error", "Customer not found")

    def enter_code(self):
        code = self.code_var.get()
        self.code_var.set("")  # Clear the code field
        cursor.execute("SELECT * FROM users WHERE code = ?", (code,))
        customer = cursor.fetchone()
        if customer:
            end_date = datetime.strptime(customer[7], "%Y-%m-%d")
            if end_date < datetime.now():
                messagebox.showerror("Error", "Your membership has expired")
            self.show_customer_info(customer)
        else:
            messagebox.showerror("Error", "Customer not found")

    def show_customer_info(self, customer):
        info_window = tk.Toplevel(self.root)
        info_window.title("Customer Info")
        info_window.configure(bg="white")
        info_window.iconbitmap("Gym.ico")
        try:
            img = Image.open(customer[4])
            img = img.resize((60, 60), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(info_window, image=photo, bg="white").pack(pady=10)
            info_window.image = photo  # Keep a reference to avoid garbage collection
        except FileNotFoundError:
            tk.Label(info_window, text="No Photo", bg="white", fg="blue", width=10, height=5, relief="solid").pack(pady=10)
        tk.Label(info_window, text=f"Name: {customer[1]}", bg="white", fg="blue").pack(pady=10)
        tk.Label(info_window, text=f"Start Date: {customer[6]}", bg="white", fg="blue").pack(pady=10)
        tk.Label(info_window, text=f"End Date: {customer[7]}", bg="white", fg="blue").pack(pady=10)
        tk.Button(info_window, text="Delete Member", command=lambda: self.delete_member(customer, info_window), bg="blue", fg="white").pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(info_window, text="Update Member", command=lambda: self.update_member(customer, info_window), bg="blue", fg="white").pack(side=tk.RIGHT, padx=10, pady=10)

    def delete_member(self, customer, window):
        cursor.execute("DELETE FROM users WHERE code = ?", (customer[0],))
        connection.commit()
        window.destroy()
        self.refresh_table()

    def update_member(self, customer, window):
        window.destroy()
        self.add_new_member(customer)

    def add_new_member(self, customer=None):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Member")
        add_window.configure(bg="white")
        add_window.iconbitmap("Gym.ico")

        tk.Label(add_window, text="Name:", bg="white", fg="blue").grid(row=0, column=0, padx=10, pady=10)
        name_var = tk.StringVar(value=customer[1] if customer else "")
        tk.Entry(add_window, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Age:", bg="white", fg="blue").grid(row=1, column=0, padx=10, pady=10)
        age_var = tk.IntVar(value=customer[5] if customer else 0)
        tk.Entry(add_window, textvariable=age_var).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Gender:", bg="white", fg="blue").grid(row=2, column=0, padx=10, pady=10)
        gender_var = tk.StringVar(value=customer[2] if customer else "Male")
        tk.Radiobutton(add_window, text="Male", variable=gender_var, value="Male", bg="white", fg="blue").grid(row=2, column=1, padx=10, pady=10)
        tk.Radiobutton(add_window, text="Female", variable=gender_var, value="Female", bg="white", fg="blue").grid(row=2, column=2, padx=10, pady=10)

        tk.Label(add_window, text="Amount:", bg="white", fg="blue").grid(row=3, column=0, padx=10, pady=10)
        amount_var = tk.DoubleVar(value=customer[3] if customer else 0.0)
        tk.Entry(add_window, textvariable=amount_var).grid(row=3, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Start Date:", bg="white", fg="blue").grid(row=4, column=0, padx=10, pady=10)
        start_date_var = tk.StringVar(value=customer[6] if customer else "")
        DateEntry(add_window, textvariable=start_date_var, date_pattern='yyyy-mm-dd').grid(row=4, column=1, padx=10, pady=10)

        tk.Label(add_window, text="End Date:", bg="white", fg="blue").grid(row=5, column=0, padx=10, pady=10)
        end_date_var = tk.StringVar(value=customer[7] if customer else "")
        DateEntry(add_window, textvariable=end_date_var, date_pattern='yyyy-mm-dd').grid(row=5, column=1, padx=10, pady=10)

        tk.Label(add_window, text="4-Digit Code:", bg="white", fg="blue").grid(row=6, column=0, padx=10, pady=10)
        code_var = tk.StringVar(value=customer[0] if customer else "")
        tk.Entry(add_window, textvariable=code_var).grid(row=6, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Photo:", bg="white", fg="blue").grid(row=7, column=0, padx=10, pady=10)
        photo_var = tk.StringVar(value=customer[4] if customer else "")
        tk.Entry(add_window, textvariable=photo_var, state='readonly').grid(row=7, column=1, padx=10, pady=10)
        tk.Button(add_window, text="Browse", command=lambda: self.browse_photo(photo_var), bg="blue", fg="white").grid(row=7, column=2, padx=10, pady=10)

        tk.Button(add_window, text="Add", command=lambda: self.save_member(name_var, age_var, gender_var, amount_var, start_date_var, end_date_var, code_var, photo_var, add_window, customer), bg="blue", fg="white").grid(row=8, column=0, columnspan=3, padx=10, pady=10)

    def browse_photo(self, photo_var):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            photo_var.set(file_path)

    def save_member(self, name_var, age_var, gender_var, amount_var, start_date_var, end_date_var, code_var, photo_var, window, existing_customer=None):
        if len(code_var.get()) != 4 or not code_var.get().isdigit():
            messagebox.showerror("Error", "Code must be a 4-digit number")
            return
        if existing_customer:
            cursor.execute("""
                UPDATE users
                SET name = ?, age = ?, gender = ?, amount = ?, start_date = ?, end_date = ?, photo = ?
                WHERE code = ?
            """, (name_var.get(), age_var.get(), gender_var.get(), amount_var.get(), start_date_var.get(), end_date_var.get(), photo_var.get(), code_var.get()))
        else:
            cursor.execute("""
                INSERT INTO users (name, age, gender, amount, start_date, end_date, photo, code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name_var.get(), age_var.get(), gender_var.get(), amount_var.get(), start_date_var.get(), end_date_var.get(), photo_var.get(), code_var.get()))
        connection.commit()
        window.destroy()
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.populate_table()

    def delete_all_data(self):
        cursor.execute("DELETE FROM users")
        connection.commit()
        self.refresh_table()

    def navigate_to_page(self, selected_page):
        self.root.destroy()
        if selected_page == "Home":
            root = tk.Tk()
            GymApp(root)
            root.mainloop()
        elif selected_page == "Employee":
            root = tk.Tk()
            EmployeePage(root)
            root.mainloop()
        elif selected_page == "Trainers":
            root = tk.Tk()
            TrainersPage(root)
            root.mainloop()
        elif selected_page == "Salaries":
            root = tk.Tk()
            salariesPage(root)
            root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = GymApp(root)
    root.mainloop()