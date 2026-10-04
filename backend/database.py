import sqlite3

DATABASE_NAME = "appointme.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    # PATIENT / USER TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    # HOSPITALS TABLE
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

    # DOCTORS TABLE
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

    # DOCTOR LOGIN ACCOUNTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctor_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER UNIQUE NOT NULL,
        login_id TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Pending',
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
    """)

    cursor.execute("PRAGMA table_info(doctor_accounts)")
    doctor_account_columns = [
        column[1] for column in cursor.fetchall()
    ]

    if "status" not in doctor_account_columns:
        cursor.execute("""
        ALTER TABLE doctor_accounts
        ADD COLUMN status TEXT NOT NULL DEFAULT 'Pending'
        """)

    # ADMIN LOGIN ACCOUNTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login_id TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # APPOINTMENTS TABLE
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

    # FEEDBACK TABLE
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

    # EXISTING DOCTOR ACCOUNTS
    cursor.execute("SELECT id FROM doctors")
    doctors = cursor.fetchall()

    for doctor in doctors:
        doctor_id = doctor[0]
        login_id = f"DR{doctor_id}"

        cursor.execute("""
        INSERT OR IGNORE INTO doctor_accounts
        (doctor_id, login_id, password, status)
        VALUES (?, ?, ?, ?)
        """, (
            doctor_id,
            login_id,
            "Doctor@123",
            "Approved"
        ))

    # EXISTING ADMIN ACCOUNT
    cursor.execute("""
    INSERT OR IGNORE INTO admin_accounts
    (login_id, password)
    VALUES (?, ?)
    """, (
        "ADMIN001",
        "Admin@123"
    ))

    connection.commit()
    connection.close()


# PATIENT FUNCTIONS

def add_user(name, email, password, phone):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO users
        (name, email, password, phone)
        VALUES (?, ?, ?, ?)
        """, (
            name,
            email,
            password,
            phone
        ))

        connection.commit()

    finally:
        connection.close()


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


# HOSPITAL FUNCTIONS

def add_hospital(name, address, phone, rating, speciality):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO hospitals
    (name, address, phone, rating, speciality)
    VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        address,
        phone,
        rating,
        speciality
    ))

    connection.commit()
    connection.close()


def get_all_hospitals():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM hospitals")
    hospitals = cursor.fetchall()

    connection.close()

    return hospitals


# DOCTOR FUNCTIONS

def add_doctor(
    name,
    specialization,
    experience,
    degrees,
    hospital_id
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO doctors
    (name, specialization, experience, degrees, hospital_id)
    VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        specialization,
        experience,
        degrees,
        hospital_id
    ))

    doctor_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return doctor_id


def add_doctor_account(
    doctor_id,
    login_id,
    password
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO doctor_accounts
    (doctor_id, login_id, password, status)
    VALUES (?, ?, ?, ?)
    """, (
        doctor_id,
        login_id,
        password,
        "Pending"
    ))

    connection.commit()
    connection.close()


def get_all_doctors():
    connection = get_connection()
    cursor = connection.cursor()

    # Only approved doctors should be visible to patients.
    cursor.execute("""
    SELECT doctors.*
    FROM doctors
    JOIN doctor_accounts
    ON doctors.id = doctor_accounts.doctor_id
    WHERE doctor_accounts.status = 'Approved'
    """)

    doctors = cursor.fetchall()

    connection.close()

    return doctors


def get_doctor_by_login_id(login_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT doctor_accounts.id,
           doctor_accounts.doctor_id,
           doctor_accounts.login_id,
           doctor_accounts.password,
           doctor_accounts.status,
           doctors.name,
           doctors.specialization,
           doctors.experience,
           doctors.degrees,
           doctors.hospital_id
    FROM doctor_accounts
    JOIN doctors
    ON doctor_accounts.doctor_id = doctors.id
    WHERE doctor_accounts.login_id = ?
    """, (login_id,))

    doctor = cursor.fetchone()

    connection.close()

    return doctor


# ADMIN FUNCTIONS

def get_admin_by_login_id(login_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id,
           login_id,
           password
    FROM admin_accounts
    WHERE login_id = ?
    """, (login_id,))

    admin = cursor.fetchone()

    connection.close()

    return admin


def add_admin(login_id, password):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO admin_accounts
    (login_id, password)
    VALUES (?, ?)
    """, (
        login_id,
        password
    ))

    connection.commit()
    connection.close()


# APPOINTMENT FUNCTIONS

def cancel_appointment(appointment_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE appointments
    SET status = ?
    WHERE id = ?
    """, (
        "Cancelled",
        appointment_id
    ))

    connection.commit()
    connection.close()