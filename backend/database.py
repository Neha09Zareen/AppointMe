import sqlite3

DATABASE_NAME = "appointme.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    # Hospitals table
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

    # Doctors table
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

    # Appointments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Booked',
        FOREIGN KEY (patient_id) REFERENCES users(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
    """)

    # Feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        comments TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending',
        FOREIGN KEY (patient_id) REFERENCES users(id)
    )
    """)

    connection.commit()
    connection.close()


def add_user(name, email, password, phone):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO users (name, email, password, phone)
        VALUES (?, ?, ?, ?)
        """, (name, email, password, phone))

        connection.commit()

    finally:
        connection.close()


def add_hospital(name, address, phone, rating, speciality):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO hospitals
    (name, address, phone, rating, speciality)
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


def cancel_appointment(appointment_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE appointments
    SET status = ?
    WHERE id = ?
    """, ("Cancelled", appointment_id))

    connection.commit()
    connection.close()