from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from database import (
    create_tables,
    add_user,
    get_user_by_email,
    get_doctor_by_login_id,
    get_admin_by_login_id,
    add_admin,
    get_all_hospitals,
    get_all_doctors,
    get_connection
)


app = Flask(__name__)
CORS(app)


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return "Welcome to AppointMe Backend!"


# =========================
# PATIENT REGISTER
# =========================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    try:
        add_user(
            data["name"],
            data["email"],
            data["password"],
            data["phone"]
        )

        user = get_user_by_email(data["email"])

        return jsonify({
            "message": "Registration Successful",
            "user_id": user[0],
            "name": user[1],
            "email": user[2]
        })

    except Exception as error:
        print("Registration error:", error)

        return jsonify({
            "message": "Email already registered"
        }), 400


# =========================
# PATIENT LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = get_user_by_email(data["email"])

    if user is None:
        return jsonify({
            "message": "User not found"
        })

    if user[3] != data["password"]:
        return jsonify({
            "message": "Incorrect password"
        })

    return jsonify({
        "message": "Login Successful",
        "user_id": user[0],
        "name": user[1],
        "email": user[2]
    })


# =========================
# DOCTOR REGISTER
# =========================

@app.route("/doctor-register", methods=["POST"])
def doctor_register():
    data = request.get_json()

    try:
        name = data["name"]
        email = data["email"]
        password = data["password"]
        phone = data["phone"]
        specialization = data["specialization"]
        experience = data["experience"]
        degrees = data["degrees"]
        hospital_id = data["hospital_id"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM doctor_accounts WHERE login_id = ?",
            (email,)
        )

        existing_doctor = cursor.fetchone()

        if existing_doctor:
            connection.close()

            return jsonify({
                "message": "Doctor account already exists"
            }), 400

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        )

        existing_patient = cursor.fetchone()

        if existing_patient:
            connection.close()

            return jsonify({
                "message": "This email is already registered as a patient account"
            }), 400

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

        cursor.execute("""
            INSERT INTO doctor_accounts
            (doctor_id, login_id, password, status)
            VALUES (?, ?, ?, ?)
        """, (
            doctor_id,
            email,
            password,
            "Pending"
        ))

        connection.commit()
        connection.close()

        return jsonify({
            "message": "Doctor registration submitted. Waiting for admin approval.",
            "doctor_id": doctor_id
        })

    except Exception as error:
        print("Doctor registration error:", error)

        return jsonify({
            "message": "Doctor registration failed"
        }), 400


# =========================
# DOCTOR LOGIN
# =========================

@app.route("/doctor-login", methods=["POST"])
def doctor_login():
    data = request.get_json()

    doctor = get_doctor_by_login_id(data["login_id"])

    if doctor is None:
        return jsonify({
            "message": "Invalid doctor login ID"
        }), 401

    if doctor[3] != data["password"]:
        return jsonify({
            "message": "Incorrect password"
        }), 401

    if doctor[4] != "Approved":
        return jsonify({
            "message": "Your doctor account is still waiting for admin approval."
        }), 403

    return jsonify({
        "message": "Doctor Login Successful",
        "doctor_id": doctor[1],
        "login_id": doctor[2],
        "name": doctor[5],
        "specialization": doctor[6],
        "experience": doctor[7],
        "degrees": doctor[8],
        "hospital_id": doctor[9]
    })


# =========================
# ADMIN REGISTER
# =========================

@app.route("/admin-register", methods=["POST"])
def admin_register():
    data = request.get_json()

    ADMIN_REGISTRATION_KEY = "APPOINTME-ADMIN"

    login_id = data.get("login_id")
    password = data.get("password")
    registration_key = data.get("registration_key")

    if not login_id or not password or not registration_key:
        return jsonify({
            "message": "All fields are required"
        }), 400

    if registration_key != ADMIN_REGISTRATION_KEY:
        return jsonify({
            "message": "Invalid admin registration key"
        }), 403

    existing_admin = get_admin_by_login_id(login_id)

    if existing_admin:
        return jsonify({
            "message": "Admin login ID already exists"
        }), 400

    try:
        add_admin(
            login_id,
            password
        )

        return jsonify({
            "message": "Admin registration successful"
        })

    except Exception as error:
        print("Admin registration error:", error)

        return jsonify({
            "message": "Admin registration failed"
        }), 400


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json()

    admin = get_admin_by_login_id(data["login_id"])

    if admin is None:
        return jsonify({
            "message": "Invalid admin login ID"
        }), 401

    if admin[2] != data["password"]:
        return jsonify({
            "message": "Incorrect password"
        }), 401

    return jsonify({
        "message": "Admin Login Successful",
        "admin_id": admin[0],
        "login_id": admin[1]
    })


# =========================
# ADMIN - PENDING DOCTORS
# =========================

@app.route("/admin/pending-doctors", methods=["GET"])
def get_pending_doctors():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            doctor_accounts.id,
            doctors.id,
            doctors.name,
            doctor_accounts.login_id,
            doctors.specialization,
            doctors.experience,
            doctors.degrees,
            doctors.hospital_id,
            doctor_accounts.status
        FROM doctor_accounts
        JOIN doctors
        ON doctor_accounts.doctor_id = doctors.id
        WHERE doctor_accounts.status = 'Pending'
        ORDER BY doctor_accounts.id DESC
    """)

    doctors = cursor.fetchall()

    connection.close()

    return jsonify([
        {
            "account_id": doctor[0],
            "doctor_id": doctor[1],
            "name": doctor[2],
            "email": doctor[3],
            "specialization": doctor[4],
            "experience": doctor[5],
            "degrees": doctor[6],
            "hospital_id": doctor[7],
            "status": doctor[8]
        }
        for doctor in doctors
    ])


# =========================
# ADMIN - APPROVE DOCTOR
# =========================

@app.route("/admin/doctors/<int:doctor_id>/approve", methods=["PUT"])
def approve_doctor(doctor_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE doctor_accounts
        SET status = 'Approved'
        WHERE doctor_id = ?
        AND status = 'Pending'
    """, (doctor_id,))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        return jsonify({
            "message": "Pending doctor account not found"
        }), 404

    connection.close()

    return jsonify({
        "message": "Doctor approved successfully"
    })


# =========================
# ADMIN - REJECT DOCTOR
# =========================

@app.route("/admin/doctors/<int:doctor_id>/reject", methods=["PUT"])
def reject_doctor(doctor_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE doctor_accounts
        SET status = 'Rejected'
        WHERE doctor_id = ?
        AND status = 'Pending'
    """, (doctor_id,))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        return jsonify({
            "message": "Pending doctor account not found"
        }), 404

    connection.close()

    return jsonify({
        "message": "Doctor rejected successfully"
    })


# =========================
# HOSPITALS
# =========================

@app.route("/hospitals", methods=["GET"])
def get_hospitals():
    hospitals = get_all_hospitals()

    return jsonify([
        {
            "id": hospital[0],
            "name": hospital[1],
            "address": hospital[2],
            "phone": hospital[3],
            "rating": hospital[4],
            "speciality": hospital[5]
        }
        for hospital in hospitals
    ])


# =========================
# DOCTORS
# =========================

@app.route("/doctors", methods=["GET"])
def get_doctors():
    doctors = get_all_doctors()

    return jsonify([
        {
            "id": doctor[0],
            "name": doctor[1],
            "specialization": doctor[2],
            "experience": doctor[3],
            "degrees": doctor[4],
            "hospital_id": doctor[5]
        }
        for doctor in doctors
    ])


@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    doctors = get_all_doctors()

    for doctor in doctors:
        if doctor[0] == doctor_id:
            return jsonify({
                "id": doctor[0],
                "name": doctor[1],
                "specialization": doctor[2],
                "experience": doctor[3],
                "degrees": doctor[4],
                "hospital_id": doctor[5]
            })

    return jsonify({
        "error": "Doctor not found"
    }), 404


# =========================
# BOOK APPOINTMENT
# =========================

@app.route("/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json()

    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    appointment_date = data.get("appointment_date")
    appointment_time = data.get("appointment_time")

    # Validate required fields
    if not patient_id or not doctor_id or not appointment_date or not appointment_time:
        return jsonify({
            "message": "Patient, doctor, date and time are required."
        }), 400

    # Allowed appointment slots
    allowed_time_slots = {
        "09:00",
        "10:00",
        "11:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00"
    }

    if appointment_time not in allowed_time_slots:
        return jsonify({
            "message": "Invalid appointment time slot."
        }), 400

    # Validate appointment date format
    try:
        selected_date = datetime.strptime(
            appointment_date,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return jsonify({
            "message": "Invalid appointment date format."
        }), 400

    # Get current date and time
    current_datetime = datetime.now()

    today = current_datetime.date()

    # Reject past dates
    if selected_date < today:
        return jsonify({
            "message": "Cannot book an appointment for a past date."
        }), 400

    # If appointment is today, reject already-passed times
    if selected_date == today:

        selected_datetime = datetime.strptime(
            f"{appointment_date} {appointment_time}",
            "%Y-%m-%d %H:%M"
        )

        if selected_datetime <= current_datetime:
            return jsonify({
                "message": "This appointment time has already passed."
            }), 400

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether patient exists
    cursor.execute(
        "SELECT id FROM users WHERE id = ?",
        (patient_id,)
    )

    patient = cursor.fetchone()

    if patient is None:
        connection.close()

        return jsonify({
            "message": "Patient not found."
        }), 404

    # Check whether doctor exists and is approved
    cursor.execute("""
        SELECT doctors.id
        FROM doctors
        JOIN doctor_accounts
        ON doctors.id = doctor_accounts.doctor_id
        WHERE doctors.id = ?
        AND doctor_accounts.status = 'Approved'
    """, (doctor_id,))

    doctor = cursor.fetchone()

    if doctor is None:
        connection.close()

        return jsonify({
            "message": "Doctor not found or not approved."
        }), 404

    # Prevent double-booking the same doctor
    cursor.execute("""
        SELECT id
        FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND status != 'Cancelled'
    """, (
        doctor_id,
        appointment_date,
        appointment_time
    ))

    existing_appointment = cursor.fetchone()

    if existing_appointment:
        connection.close()

        return jsonify({
            "message": "This time slot is already booked for this doctor."
        }), 409

    # Create appointment
    cursor.execute("""
        INSERT INTO appointments
        (patient_id, doctor_id, appointment_date, appointment_time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        "Booked"
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Appointment booked successfully"
    })


# =========================
# CANCEL APPOINTMENT
# =========================

@app.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def cancel_appointment(appointment_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE appointments
        SET status = ?
        WHERE id = ?
    """, ("Cancelled", appointment_id))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()

        return jsonify({
            "message": "Appointment not found"
        }), 404

    connection.close()

    return jsonify({
        "message": "Appointment cancelled successfully"
    })


# =========================
# RESCHEDULE APPOINTMENT
# =========================

@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def reschedule_appointment(appointment_id):
    data = request.get_json()

    appointment_date = data.get("appointment_date")
    appointment_time = data.get("appointment_time")

    # Validate required fields
    if not appointment_date or not appointment_time:
        return jsonify({
            "message": "Appointment date and time are required."
        }), 400

    # Allowed appointment slots
    allowed_time_slots = {
        "09:00",
        "10:00",
        "11:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00"
    }

    if appointment_time not in allowed_time_slots:
        return jsonify({
            "message": "Invalid appointment time slot."
        }), 400

    # Validate appointment date format
    try:
        selected_date = datetime.strptime(
            appointment_date,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return jsonify({
            "message": "Invalid appointment date format."
        }), 400

    current_datetime = datetime.now()
    today = current_datetime.date()

    # Reject past dates
    if selected_date < today:
        return jsonify({
            "message": "Cannot reschedule to a past date."
        }), 400

    # Reject already-passed time if rescheduling for today
    if selected_date == today:

        selected_datetime = datetime.strptime(
            f"{appointment_date} {appointment_time}",
            "%Y-%m-%d %H:%M"
        )

        if selected_datetime <= current_datetime:
            return jsonify({
                "message": "This appointment time has already passed."
            }), 400

    connection = get_connection()
    cursor = connection.cursor()

    # Get the existing appointment
    cursor.execute("""
        SELECT doctor_id, status
        FROM appointments
        WHERE id = ?
    """, (appointment_id,))

    appointment = cursor.fetchone()

    if appointment is None:
        connection.close()

        return jsonify({
            "message": "Appointment not found."
        }), 404

    doctor_id = appointment[0]
    current_status = appointment[1]

    # Do not reschedule a cancelled appointment
    if current_status == "Cancelled":
        connection.close()

        return jsonify({
            "message": "Cancelled appointments cannot be rescheduled."
        }), 400

    # Prevent double-booking the doctor
    cursor.execute("""
        SELECT id
        FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND id != ?
        AND status != 'Cancelled'
    """, (
        doctor_id,
        appointment_date,
        appointment_time,
        appointment_id
    ))

    existing_appointment = cursor.fetchone()

    if existing_appointment:
        connection.close()

        return jsonify({
            "message": "This time slot is already booked for this doctor."
        }), 409

    # Update appointment
    cursor.execute("""
        UPDATE appointments
        SET appointment_date = ?,
            appointment_time = ?,
            status = ?
        WHERE id = ?
    """, (
        appointment_date,
        appointment_time,
        "Rescheduled",
        appointment_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Appointment rescheduled successfully"
    })


# =========================
# PATIENT APPOINTMENTS
# =========================

@app.route("/appointments/<int:patient_id>", methods=["GET"])
def get_patient_appointments(patient_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id,
               patient_id,
               doctor_id,
               appointment_date,
               appointment_time,
               status
        FROM appointments
        WHERE patient_id = ?
        ORDER BY appointment_date, appointment_time
    """, (patient_id,))

    appointments = cursor.fetchall()

    connection.close()

    return jsonify([
        {
            "id": appointment[0],
            "patient_id": appointment[1],
            "doctor_id": appointment[2],
            "appointment_date": appointment[3],
            "appointment_time": appointment[4],
            "status": appointment[5]
        }
        for appointment in appointments
    ])


# =========================
# DOCTOR APPOINTMENTS
# =========================

@app.route("/doctor-appointments/<int:doctor_id>", methods=["GET"])
def get_doctor_appointments(doctor_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT appointments.id,
               appointments.patient_id,
               users.name,
               appointments.appointment_date,
               appointments.appointment_time,
               appointments.status
        FROM appointments
        JOIN users
        ON appointments.patient_id = users.id
        WHERE appointments.doctor_id = ?
        ORDER BY appointments.appointment_date,
                 appointments.appointment_time
    """, (doctor_id,))

    appointments = cursor.fetchall()

    connection.close()

    return jsonify([
        {
            "id": appointment[0],
            "patient_id": appointment[1],
            "patient_name": appointment[2],
            "appointment_date": appointment[3],
            "appointment_time": appointment[4],
            "status": appointment[5]
        }
        for appointment in appointments
    ])


# =========================
# ADMIN - ALL APPOINTMENTS
# =========================

@app.route("/admin/appointments", methods=["GET"])
def get_all_admin_appointments():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            appointments.id,
            appointments.patient_id,
            users.name,
            appointments.doctor_id,
            doctors.name,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status
        FROM appointments
        JOIN users
        ON appointments.patient_id = users.id
        JOIN doctors
        ON appointments.doctor_id = doctors.id
        WHERE appointments.status != 'Cancelled'
        ORDER BY appointments.id ASC
    """)

    appointments = cursor.fetchall()

    connection.close()

    return jsonify([
        {
            "serial_number": index + 1,
            "id": appointment[0],
            "patient_id": appointment[1],
            "patient_name": appointment[2],
            "doctor_id": appointment[3],
            "doctor_name": appointment[4],
            "appointment_date": appointment[5],
            "appointment_time": appointment[6],
            "status": appointment[7]
        }
        for index, appointment in enumerate(appointments)
    ])


# =========================
# SUBMIT FEEDBACK
# =========================

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()

    patient_id = data["patient_id"]
    rating = data["rating"]
    comments = data["comments"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback
        (patient_id, rating, comments, status)
        VALUES (?, ?, ?, ?)
    """, (
        patient_id,
        rating,
        comments,
        "Pending"
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "message": "Feedback submitted successfully"
    })


# =========================
# ADMIN STATISTICS
# =========================

@app.route("/admin-stats", methods=["GET"])
def get_admin_stats():
    connection = get_connection()
    cursor = connection.cursor()

    # Count only approved doctors
    cursor.execute("""
        SELECT COUNT(*)
        FROM doctor_accounts
        WHERE status = 'Approved'
    """)

    total_doctors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")

    total_patients = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM appointments
        WHERE appointment_date = DATE('now')
    """)

    appointments_today = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM feedback
        WHERE status = 'Pending'
    """)

    pending_feedback = cursor.fetchone()[0]

    connection.close()

    return jsonify({
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "appointments_today": appointments_today,
        "pending_feedback": pending_feedback
    })


# =========================
# START SERVER
# =========================

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)