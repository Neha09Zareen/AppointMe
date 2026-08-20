import sqlite3

DATABASE_NAME = "appointme.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hospitals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone TEXT NOT NULL,
    rating REAL,
    speciality TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    experience INTEGER,
    degrees TEXT,
    hospital_id INTEGER,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
    )
    """)

    connection.commit()
    connection.close()

def add_user(name, email, password, phone):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO users (name, email, password, phone)
    VALUES (?, ?, ?, ?)
    """, (name, email, password, phone))

    connection.commit()
    connection.close()

def add_hospital(name, address, phone, rating, speciality):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO hospitals (name, address, phone, rating, speciality)
    VALUES (?, ?, ?, ?, ?)
    """, (name, address, phone, rating, speciality))

    connection.commit()
    connection.close()

def get_all_hospitals():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM hospitals")

    hospitals = cursor.fetchall()

    connection.close()

    return hospitals

def add_doctor(name, specialization, experience, degrees, hospital_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO doctors
    (name, specialization, experience, degrees, hospital_id)
    VALUES (?, ?, ?, ?, ?)
    """, (name, specialization, experience, degrees, hospital_id))

    connection.commit()
    connection.close()

def get_all_doctors():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM doctors")

    doctors = cursor.fetchall()

    connection.close()

    return doctors


def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    return user
