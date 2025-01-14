import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("gym.db")

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    code INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NUll,
    amount INTEGER NOT NULL,
    photo TEXT,
    age INTEGER,
    start_date TEXT NOT NULL DEFAULT (strftime('%d/%m/%Y', 'now')),
    end_date TEXT NOt NULL
)
""")

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


# Commit changes and close the connection
connection.commit()
connection.close()
