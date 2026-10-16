import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None
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
    try:
        data = request.get_json()

<<<<<<< HEAD
        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")

        if not name or not email or not password or not phone:
            return jsonify({
                "message": "All fields are required"
            }), 400

        add_user(name, email, password, phone)

        return jsonify({
            "message": "Registration Successful"
        }), 201

    except Exception as error:
        print("REGISTER ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# LOGIN
=======
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
>>>>>>> origin/main
# =========================

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "message": "Email and password are required"
            }), 400

        user = get_user_by_email(email)

        if user is None:
            return jsonify({
                "message": "User not found"
            }), 404

        if user[3] != password:
            return jsonify({
                "message": "Incorrect password"
            }), 401

        return jsonify({
            "message": "Login Successful",
            "user_id": user[0],
            "name": user[1],
            "email": user[2]
        }), 200

    except Exception as error:
        print("LOGIN ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500

<<<<<<< HEAD

# =========================
# HOSPITALS
# =========================
=======
    return jsonify({
        "message": "Login Successful",
        "user_id": user[0],
        "name": user[1],
        "email": user[2]
    })
>>>>>>> origin/main


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
    try:
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
        ]), 200

    except Exception as error:
        print("HOSPITAL ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# ALL DOCTORS
# =========================


# =========================
# DOCTORS
# =========================

@app.route("/doctors", methods=["GET"])
def get_doctors():
    try:
        doctors = get_all_doctors()

<<<<<<< HEAD
        return jsonify([
            {
=======
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
>>>>>>> origin/main
                "id": doctor[0],
                "name": doctor[1],
                "specialization": doctor[2],
                "experience": doctor[3],
                "degrees": doctor[4],
                "hospital_id": doctor[5]
            }
            for doctor in doctors
        ]), 200

<<<<<<< HEAD
    except Exception as error:
        print("DOCTORS ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# SINGLE DOCTOR
# =========================

@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    try:
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
                }), 200

        return jsonify({
            "message": "Doctor not found"
        }), 404

    except Exception as error:
        print("DOCTOR ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500
=======
    return jsonify({
        "error": "Doctor not found"
    }), 404
>>>>>>> origin/main


# =========================
# BOOK APPOINTMENT
# =========================
<<<<<<< HEAD

@app.route("/appointments", methods=["POST"])
def book_appointment_route():
    try:
        data = request.get_json()

        print("BOOKING DATA RECEIVED:", data)

        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        # Accept user_id from frontend
        user_id = data.get("user_id")

        doctor_id = data.get("doctor_id")
        hospital_id = data.get("hospital_id")
        appointment_date = data.get("appointment_date")
        appointment_time = data.get("appointment_time")

        if user_id is None:
            # Keep compatibility with the current frontend
            user_id = data.get("patient_id")

        if user_id is None:
            return jsonify({
                "message": "User ID is required"
            }), 400

        # Check if user exists before creating the appointment
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id
            FROM users
            WHERE id = ?
        """, (int(user_id),))

        user = cursor.fetchone()
        connection.close()

        if user is None:
            return jsonify({
                "message": "User not found"
            }), 404

        if doctor_id is None:
            return jsonify({
                "message": "Doctor ID is required"
            }), 400

        if hospital_id is None:
            # Get hospital automatically from doctor
            doctors = get_all_doctors()

            doctor = next(
                (d for d in doctors if d[0] == int(doctor_id)),
                None
            )

            if doctor is None:
                return jsonify({
                    "message": "Doctor not found"
                }), 404

            hospital_id = doctor[5]

        if not appointment_date:
            return jsonify({
                "message": "Appointment date is required"
            }), 400

        if not appointment_time:
            return jsonify({
                "message": "Appointment time is required"
            }), 400

        appointment_id = book_appointment(
            int(user_id),
            int(doctor_id),
            int(hospital_id),
            appointment_date,
            appointment_time
        )

        print("APPOINTMENT BOOKED:", appointment_id)

        return jsonify({
            "message": "Appointment booked successfully",
            "appointment_id": appointment_id
        }), 201

    except Exception as error:
        print("BOOKING ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# GET PATIENT APPOINTMENTS
# =========================

@app.route("/appointments/<int:user_id>", methods=["GET"])
def get_patient_appointments(user_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                user_id,
                doctor_id,
                hospital_id,
                appointment_date,
                appointment_time,
                status
            FROM appointments
            WHERE user_id = ?
            ORDER BY appointment_date, appointment_time
        """, (user_id,))

        appointments = cursor.fetchall()

        connection.close()

        return jsonify([
            {
                "id": appointment[0],
                "user_id": appointment[1],
                "doctor_id": appointment[2],
                "hospital_id": appointment[3],
                "appointment_date": appointment[4],
                "appointment_time": appointment[5],
                "status": appointment[6]
            }
            for appointment in appointments
        ]), 200

    except Exception as error:
        print("APPOINTMENT HISTORY ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500

=======


def generate_symptom_summary(symptoms):
    if not gemini_client:
        raise RuntimeError("GEMINI_API_KEY is missing from backend .env")

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""
Create a concise symptom summary for a doctor.

Rules:
- Use short bullet points.
- List each symptom separately.
- Include duration only when explicitly mentioned.
- Do not diagnose, prescribe, or invent details.
- Do not add disclaimers or extra notes.

Patient-reported symptoms:
{symptoms}
"""
    )

    summary = (response.text or "").strip()

    if not summary:
        raise RuntimeError("Gemini returned an empty summary.")

    return summary

@app.route("/symptom-summary", methods=["POST"])
def preview_symptom_summary():
    data = request.get_json() or {}
    symptoms = (data.get("symptoms") or "").strip()

    if not symptoms:
        return jsonify({"message": "Please enter your symptoms."}), 400

    try:
        summary = generate_symptom_summary(symptoms)
        return jsonify({"summary": summary})
    except Exception as error:
        print("Gemini summary error:", error)
        return jsonify({
            "message": "Could not generate the AI symptom summary. Please try again."
        }), 502

@app.route("/appointments", methods=["POST"])

def book_appointment():
    data = request.get_json() or {}

    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    appointment_date = data.get("appointment_date")
    appointment_time = data.get("appointment_time")
    symptoms = (data.get("symptoms") or "").strip()
    symptom_summary = ""

    if not all([patient_id, doctor_id, appointment_date, appointment_time]):
        return jsonify({
            "message": "Patient, doctor, date and time are required."
        }), 400

    if not symptoms:
        return jsonify({"message": "Please enter your symptoms."}), 400

    try:
        symptom_summary = generate_symptom_summary(symptoms)
    except Exception as error:
        print("Gemini summary error:", error)
        return jsonify({
            "message": "Could not generate the AI symptom summary. Please try again."
        }), 502

    allowed_time_slots = {
        "09:00", "10:00", "11:00", "14:00", "15:00",
        "16:00", "17:00", "18:00", "19:00", "20:00"
    }

    if appointment_time not in allowed_time_slots:
        return jsonify({"message": "Invalid appointment time slot."}), 400

    try:
        selected_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid appointment date format."}), 400

    now = datetime.now()

    if selected_date < now.date():
        return jsonify({"message": "Cannot book an appointment for a past date."}), 400

    if selected_date == now.date():
        selected_datetime = datetime.strptime(
            f"{appointment_date} {appointment_time}", "%Y-%m-%d %H:%M"
        )
        if selected_datetime <= now:
            return jsonify({"message": "This appointment time has already passed."}), 400

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM users WHERE id = ?", (patient_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "Patient not found."}), 404

        cursor.execute("""
            SELECT doctors.id
            FROM doctors
            JOIN doctor_accounts ON doctors.id = doctor_accounts.doctor_id
            WHERE doctors.id = ? AND doctor_accounts.status = 'Approved'
        """, (doctor_id,))

        if cursor.fetchone() is None:
            return jsonify({"message": "Doctor not found or not approved."}), 404

        cursor.execute("""
            SELECT id FROM appointments
            WHERE doctor_id = ?
            AND appointment_date = ?
            AND appointment_time = ?
            AND status != 'Cancelled'
        """, (doctor_id, appointment_date, appointment_time))

        if cursor.fetchone():
            return jsonify({"message": "This time slot is already booked."}), 409

        cursor.execute("PRAGMA table_info(appointments)")
        columns = {row[1] for row in cursor.fetchall()}

        if "symptoms" not in columns or "symptom_summary" not in columns:
            return jsonify({
                "message": "Database columns are missing. Update the appointments table first."
            }), 500

        cursor.execute("""
            INSERT INTO appointments (
                patient_id, doctor_id, appointment_date,
                appointment_time, status, symptoms, symptom_summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id, doctor_id, appointment_date,
            appointment_time, "Booked", symptoms, symptom_summary
        ))

        connection.commit()

        return jsonify({"message": "Appointment booked successfully"}), 201

    except Exception as error:
        connection.rollback()
        print("Booking error:", error)
        return jsonify({"message": "Booking failed. Check the backend terminal."}), 500

    finally:
        connection.close()

>>>>>>> origin/main

# =========================
# CANCEL APPOINTMENT
# =========================

@app.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def cancel_appointment_api(appointment_id):
    try:
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

        if cursor.rowcount == 0:
            connection.close()

            return jsonify({
                "message": "Appointment not found"
            }), 404

        connection.close()

        return jsonify({
            "message": "Appointment cancelled successfully"
        }), 200

    except Exception as error:
        print("CANCEL ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# RESCHEDULE APPOINTMENT
# =========================


# =========================
# RESCHEDULE APPOINTMENT
# =========================

@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def reschedule_appointment_api(appointment_id):
    try:
        data = request.get_json()

<<<<<<< HEAD
        if not data:
            return jsonify({
                "message": "No data received"
=======
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
>>>>>>> origin/main
            }), 400

        appointment_date = data.get("appointment_date")
        appointment_time = data.get("appointment_time")

<<<<<<< HEAD
        if not appointment_date or not appointment_time:
            return jsonify({
                "message": "Appointment date and time are required"
            }), 400

        # Use the database function
        reschedule_appointment(
            appointment_id,
            appointment_date,
            appointment_time
        )

        # Check whether appointment exists
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id
            FROM appointments
            WHERE id = ?
        """, (appointment_id,))

        appointment = cursor.fetchone()

        connection.close()

        if appointment is None:
            return jsonify({
                "message": "Appointment not found"
            }), 404

        return jsonify({
            "message": "Appointment rescheduled successfully"
        }), 200

    except Exception as error:
        print("RESCHEDULE ERROR:", error)
=======
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
>>>>>>> origin/main

        return jsonify({
            "message": str(error)
        }), 500

<<<<<<< HEAD

# =========================
# FEEDBACK
# =========================

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    try:
        data = request.get_json()
=======

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
>>>>>>> origin/main

        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        user_id = data.get("user_id")
        doctor_id = data.get("doctor_id")
        rating = data.get("rating")
        comment = data.get("comment")

        if user_id is None:
            return jsonify({
                "message": "User ID is required"
            }), 400

        if doctor_id is None:
            return jsonify({
                "message": "Doctor ID is required"
            }), 400

        if rating is None:
            return jsonify({
                "message": "Rating is required"
            }), 400

        if not 1 <= int(rating) <= 5:
            return jsonify({
                "message": "Rating must be between 1 and 5"
            }), 400

        connection = get_connection()
        cursor = connection.cursor()

        # Check if user exists
        cursor.execute("""
            SELECT id
            FROM users
            WHERE id = ?
        """, (int(user_id),))

        user = cursor.fetchone()

        if user is None:
            connection.close()

            return jsonify({
                "message": "User not found"
            }), 404

        # Check if doctor exists
        cursor.execute("""
            SELECT id
            FROM doctors
            WHERE id = ?
        """, (int(doctor_id),))

        doctor = cursor.fetchone()

        if doctor is None:
            connection.close()

            return jsonify({
                "message": "Doctor not found"
            }), 404

        connection.close()

        add_feedback(
            int(user_id),
            int(doctor_id),
            int(rating),
            comment
        )

        return jsonify({
            "message": "Feedback submitted successfully"
        }), 201

    except Exception as error:
        print("FEEDBACK ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# DOCTOR FEEDBACK
# =========================

@app.route("/feedback/doctor/<int:doctor_id>", methods=["GET"])
def doctor_feedback(doctor_id):
    try:
        feedback = get_doctor_feedback(doctor_id)

        result = []

        for item in feedback:
            result.append({
                "id": item[0],
                "user_id": item[1],
                "doctor_id": item[2],
                "rating": item[3],
                "comment": item[4],
                "created_at": item[5],
                "user_name": item[6]
            })

        return jsonify(result), 200

    except Exception as error:
        print("DOCTOR FEEDBACK ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# DOCTOR APPOINTMENTS
# =========================

@app.route("/doctor/<int:doctor_id>/appointments", methods=["GET"])
def doctor_appointments(doctor_id):
    try:
        appointments = get_doctor_appointments(doctor_id)

        result = []

        for appointment in appointments:
            result.append({
                "id": appointment[0],
                "user_id": appointment[1],
                "patient_name": appointment[2],
                "hospital_id": appointment[3],
                "appointment_date": appointment[4],
                "appointment_time": appointment[5],
                "status": appointment[6]
            })

        return jsonify(result), 200

    except Exception as error:
        print("DOCTOR APPOINTMENTS ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# ADMIN USERS
# =========================

@app.route("/admin/users", methods=["GET"])
def admin_users():
    try:
        users = get_all_users()

        return jsonify([
            {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "phone": user[3]
            }
            for user in users
        ]), 200

    except Exception as error:
        print("ADMIN USERS ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# ADMIN APPOINTMENTS
# =========================

@app.route("/admin/appointments", methods=["GET"])
def admin_appointments():
    try:
        appointments = get_all_appointments()

        return jsonify([
            {
                "id": appointment[0],
                "user_id": appointment[1],
                "patient_name": appointment[2],
                "doctor_id": appointment[3],
                "doctor_name": appointment[4],
                "hospital_id": appointment[5],
                "hospital_name": appointment[6],
                "appointment_date": appointment[7],
                "appointment_time": appointment[8],
                "status": appointment[9]
            }
            for appointment in appointments
        ]), 200

    except Exception as error:
        print("ADMIN APPOINTMENTS ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =========================
# START SERVER
# =========================

@app.route("/symptom-summary", methods=["POST"])
def symptom_summary():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "message": "No data received"
            }), 400

        symptoms = data.get("symptoms")

        if not symptoms or not symptoms.strip():
            return jsonify({
                "message": "Symptoms are required"
            }), 400

        prompt = f"""
You are a healthcare assistant for the AppointMe application.

Your task is ONLY to summarize the symptoms reported by the patient.
Do NOT diagnose the patient.
Do NOT suggest diseases, medications, or treatments.
Do NOT add symptoms that the patient did not mention.

Create a concise, professional summary that a doctor can quickly read.

Patient's reported symptoms:
{symptoms}

Return only the symptom summary.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return jsonify({
            "summary": response.text
        }), 200

    except Exception as error:
        print("SYMPTOM SUMMARY ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


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
       appointments.status,
       appointments.symptoms,
       appointments.symptom_summary

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
            "status": appointment[5],
            "symptoms": appointment[6],
            "symptom_summary": appointment[7]
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
<<<<<<< HEAD

    app.run(
        debug=True
    )
=======
    app.run(debug=True)
>>>>>>> origin/main
