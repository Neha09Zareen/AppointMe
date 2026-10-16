import sqlite3

DATABASE_NAME = "appointme.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
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
        user_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        hospital_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Booked',
        symptoms TEXT,
        symptom_summary TEXT,
        FOREIGN KEY (patient_id) REFERENCES users(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
    """)

    # Add missing columns to existing databases
    cursor.execute("PRAGMA table_info(appointments)")
    columns = [row[1] for row in cursor.fetchall()]

    if "symptoms" not in columns:
        cursor.execute(
            "ALTER TABLE appointments ADD COLUMN symptoms TEXT"
        )

    if "symptom_summary" not in columns:
        cursor.execute(
            "ALTER TABLE appointments ADD COLUMN symptom_summary TEXT"
        )

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


<<<<<<< HEAD
=======
# PATIENT FUNCTIONS

>>>>>>> origin/main
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

<<<<<<< HEAD

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
=======
        connection.commit()

    finally:
        connection.close()
>>>>>>> origin/main


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
def book_appointment(user_id, doctor_id, hospital_id, appointment_date, appointment_time):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO appointments
        (user_id, doctor_id, hospital_id, appointment_date, appointment_time, status)
        VALUES (?, ?, ?, ?, ?, 'Booked')
    """, (
        user_id,
        doctor_id,
        hospital_id,
        appointment_date,
        appointment_time
    ))

    connection.commit()
    appointment_id = cursor.lastrowid

    connection.close()

    return appointment_id



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
<<<<<<< HEAD
        UPDATE appointments
        SET status = 'Cancelled'
        WHERE id = ?
    """, (appointment_id,))
=======
    UPDATE appointments
    SET status = ?
    WHERE id = ?
    """, (
        "Cancelled",
        appointment_id
    ))
>>>>>>> origin/main

    connection.commit()
    connection.close()


def reschedule_appointment(appointment_id, appointment_date, appointment_time):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE appointments
        SET appointment_date = ?,
            appointment_time = ?,
            status = 'Booked'
        WHERE id = ?
    """, (
        appointment_date,
        appointment_time,
        appointment_id
    ))

    connection.commit()
    connection.close()


def get_appointment_history(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            appointments.id,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status,
            doctors.name,
            doctors.specialization,
            hospitals.name
        FROM appointments
        JOIN doctors
            ON appointments.doctor_id = doctors.id
        JOIN hospitals
            ON appointments.hospital_id = hospitals.id
        WHERE appointments.user_id = ?
        ORDER BY appointments.appointment_date DESC,
                 appointments.appointment_time DESC
    """, (user_id,))
    appointments = cursor.fetchall()

    connection.close()
    return appointments    
def add_feedback(user_id, doctor_id, rating, comment):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO feedback
    (user_id, doctor_id, rating, comment)
    VALUES (?, ?, ?, ?)
    """, (user_id, doctor_id, rating, comment))

    connection.commit()
    connection.close()


def get_doctor_feedback(doctor_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        feedback.id,
        feedback.user_id,
        feedback.doctor_id,
        feedback.rating,
        feedback.comment,
        feedback.created_at,
        users.name
    FROM feedback
    JOIN users ON feedback.user_id = users.id
    WHERE feedback.doctor_id = ?
    ORDER BY feedback.created_at DESC
    """, (doctor_id,))

    feedback = cursor.fetchall()

    connection.close()

    return feedback

def get_doctor_appointments(doctor_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        appointments.id,
        appointments.user_id,
        users.name,
        appointments.hospital_id,
        appointments.appointment_date,
        appointments.appointment_time,
        appointments.status
    FROM appointments
    JOIN users
        ON appointments.user_id = users.id
    WHERE appointments.doctor_id = ?
    ORDER BY appointments.appointment_date,
             appointments.appointment_time
    """, (doctor_id,))

    appointments = cursor.fetchall()

    connection.close()

    return appointments

def get_all_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, email, phone
        FROM users
    """)

    users = cursor.fetchall()

    connection.close()

    return users
def get_all_appointments():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            appointments.id,
            appointments.user_id,
            users.name,
            appointments.doctor_id,
            doctors.name,
            appointments.hospital_id,
            hospitals.name,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status
        FROM appointments
        JOIN users
            ON appointments.user_id = users.id
        JOIN doctors
            ON appointments.doctor_id = doctors.id
        JOIN hospitals
            ON appointments.hospital_id = hospitals.id
        ORDER BY appointments.appointment_date,
                 appointments.appointment_time
    """)

    appointments = cursor.fetchall()

    connection.close()

    return appointments