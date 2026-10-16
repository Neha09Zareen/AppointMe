
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai

from database import (
    create_tables,
    add_user,
    get_user_by_email,
    get_doctor_by_login_id,
    get_admin_by_login_id,
    add_admin,
    get_all_hospitals,
    get_all_doctors,
    get_connection,
    book_appointment,
    add_feedback,
    get_doctor_feedback,
    get_doctor_appointments,
    get_all_users,
    get_all_appointments,
)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
gemini_client = genai.Client(api_key=api_key) if api_key else None

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]}},
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)


@app.route("/", methods=["GET"])
def home():
    return "Welcome to AppointMe Backend!"


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    if not all([name, email, password, phone]):
        return jsonify({"message": "All fields are required"}), 400

    try:
        add_user(name, email, password, phone)
        user = get_user_by_email(email)
        return jsonify({
            "message": "Registration Successful",
            "user_id": user[0],
            "name": user[1],
            "email": user[2],
        }), 201
    except Exception:
        app.logger.exception("Registration failed")
        return jsonify({
            "message": "Registration failed; the email may already be registered."
        }), 400


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = get_user_by_email(email)

    if user is None:
        return jsonify({"message": "User not found"}), 404

    if user[3] != password:
        return jsonify({"message": "Incorrect password"}), 401

    return jsonify({
        "message": "Login Successful",
        "user_id": user[0],
        "name": user[1],
        "email": user[2],
    }), 200


@app.route("/doctor-register", methods=["POST"])
def doctor_register():
    data = request.get_json(silent=True) or {}

    required = [
        "name", "email", "password", "phone",
        "specialization", "experience", "degrees", "hospital_id"
    ]

    if any(data.get(key) in (None, "") for key in required):
        return jsonify({"message": "All fields are required"}), 400

    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM doctor_accounts WHERE login_id = ?",
            (data["email"],)
        )
        if cursor.fetchone():
            return jsonify({"message": "Doctor account already exists"}), 400

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (data["email"],)
        )
        if cursor.fetchone():
            return jsonify({
                "message": "This email is already registered as a patient account"
            }), 400

        cursor.execute("""
            INSERT INTO doctors
            (name, specialization, experience, degrees, hospital_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["specialization"],
            data["experience"],
            data["degrees"],
            data["hospital_id"],
        ))

        doctor_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO doctor_accounts
            (doctor_id, login_id, password, status)
            VALUES (?, ?, ?, ?)
        """, (
            doctor_id,
            data["email"],
            data["password"],
            "Pending",
        ))

        connection.commit()

        return jsonify({
            "message": "Doctor registration submitted. Waiting for admin approval.",
            "doctor_id": doctor_id,
        }), 201

    except Exception:
        app.logger.exception("Doctor registration failed")
        return jsonify({"message": "Doctor registration failed"}), 400

    finally:
        if connection is not None:
            connection.close()


@app.route("/doctor-login", methods=["POST"])
def doctor_login():
    data = request.get_json(silent=True) or {}
    login_id = data.get("login_id")
    password = data.get("password")

    if not login_id or not password:
        return jsonify({
            "message": "Login ID and password are required"
        }), 400

    doctor = get_doctor_by_login_id(login_id)

    if doctor is None:
        return jsonify({"message": "Invalid doctor login ID"}), 401

    if doctor[3] != password:
        return jsonify({"message": "Incorrect password"}), 401

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
        "hospital_id": doctor[9],
    }), 200


@app.route("/admin-register", methods=["POST"])
def admin_register():
    data = request.get_json(silent=True) or {}

    if not all(data.get(key) for key in (
        "login_id", "password", "registration_key"
    )):
        return jsonify({"message": "All fields are required"}), 400

    expected_key = os.getenv(
        "ADMIN_REGISTRATION_KEY",
        "APPOINTME-ADMIN"
    )

    if data["registration_key"] != expected_key:
        return jsonify({"message": "Invalid admin registration key"}), 403

    if get_admin_by_login_id(data["login_id"]):
        return jsonify({"message": "Admin login ID already exists"}), 400

    try:
        add_admin(data["login_id"], data["password"])
        return jsonify({"message": "Admin registration successful"}), 201
    except Exception:
        app.logger.exception("Admin registration failed")
        return jsonify({"message": "Admin registration failed"}), 400


@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or {}
    login_id = data.get("login_id")
    password = data.get("password")

    if not login_id or not password:
        return jsonify({
            "message": "Login ID and password are required"
        }), 400

    admin = get_admin_by_login_id(login_id)

    if admin is None:
        return jsonify({"message": "Invalid admin login ID"}), 401

    if admin[2] != password:
        return jsonify({"message": "Incorrect password"}), 401

    return jsonify({
        "message": "Admin Login Successful",
        "admin_id": admin[0],
        "login_id": admin[1],
    }), 200

# =========================
# ADMIN: PENDING DOCTORS
# =========================

@app.route("/admin/pending-doctors", methods=["GET"])
def get_pending_doctors():
    connection = get_connection()
    try:
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
            JOIN doctors ON doctor_accounts.doctor_id = doctors.id
            WHERE doctor_accounts.status = 'Pending'
            ORDER BY doctor_accounts.id DESC
        """)
        doctors = cursor.fetchall()

        return jsonify([
            {
                "account_id": row[0],
                "doctor_id": row[1],
                "name": row[2],
                "email": row[3],
                "specialization": row[4],
                "experience": row[5],
                "degrees": row[6],
                "hospital_id": row[7],
                "status": row[8],
            }
            for row in doctors
        ]), 200
    finally:
        connection.close()


@app.route("/admin/doctors/<int:doctor_id>/approve", methods=["PUT"])
def approve_doctor(doctor_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE doctor_accounts
            SET status = 'Approved'
            WHERE doctor_id = ? AND status = 'Pending'
        """, (doctor_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "message": "Pending doctor account not found"
            }), 404

        return jsonify({"message": "Doctor approved successfully"}), 200
    finally:
        connection.close()


@app.route("/admin/doctors/<int:doctor_id>/reject", methods=["PUT"])
def reject_doctor(doctor_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE doctor_accounts
            SET status = 'Rejected'
            WHERE doctor_id = ? AND status = 'Pending'
        """, (doctor_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "message": "Pending doctor account not found"
            }), 404

        return jsonify({"message": "Doctor rejected successfully"}), 200
    finally:
        connection.close()


# =========================
# HOSPITALS
# =========================

@app.route("/hospitals", methods=["GET"])
def get_hospitals():
    try:
        hospitals = get_all_hospitals()
        return jsonify([
            {
                "id": row[0],
                "name": row[1],
                "address": row[2],
                "phone": row[3],
                "rating": row[4],
                "speciality": row[5],
            }
            for row in hospitals
        ]), 200
    except Exception:
        app.logger.exception("Hospital retrieval failed")
        return jsonify({"message": "Could not retrieve hospitals"}), 500


# =========================
# DOCTORS
# =========================

@app.route("/doctors", methods=["GET"])
def get_doctors():
    try:
        doctors = get_all_doctors()
        return jsonify([
            {
                "id": row[0],
                "name": row[1],
                "specialization": row[2],
                "experience": row[3],
                "degrees": row[4],
                "hospital_id": row[5],
            }
            for row in doctors
        ]), 200
    except Exception:
        app.logger.exception("Doctor retrieval failed")
        return jsonify({"message": "Could not retrieve doctors"}), 500


@app.route("/doctors/<int:doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    try:
        doctors = get_all_doctors()
        doctor = next(
            (row for row in doctors if row[0] == doctor_id),
            None
        )

        if doctor is None:
            return jsonify({"message": "Doctor not found"}), 404

        return jsonify({
            "id": doctor[0],
            "name": doctor[1],
            "specialization": doctor[2],
            "experience": doctor[3],
            "degrees": doctor[4],
            "hospital_id": doctor[5],
        }), 200
    except Exception:
        app.logger.exception("Doctor retrieval failed")
        return jsonify({"message": "Could not retrieve doctor"}), 500


# =========================
# BOOK APPOINTMENT
# =========================

@app.route("/appointments", methods=["POST"])
def book_appointment_route():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id", data.get("patient_id"))
    doctor_id = data.get("doctor_id")
    hospital_id = data.get("hospital_id")
    appointment_date = data.get("appointment_date")
    appointment_time = data.get("appointment_time")

    if not all(value is not None for value in (
        user_id, doctor_id, appointment_date, appointment_time
    )):
        return jsonify({
            "message": "User ID, doctor ID, appointment date and time are required"
        }), 400

    connection = None
    try:
        user_id = int(user_id)
        doctor_id = int(doctor_id)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if cursor.fetchone() is None:
            return jsonify({"message": "User not found"}), 404

        cursor.execute(
            "SELECT id, hospital_id FROM doctors WHERE id = ?",
            (doctor_id,)
        )
        doctor = cursor.fetchone()

        if doctor is None:
            return jsonify({"message": "Doctor not found"}), 404

        if hospital_id is None:
            hospital_id = doctor[1]
        else:
            hospital_id = int(hospital_id)

        cursor.execute("""
            SELECT id FROM appointments
            WHERE doctor_id = ?
              AND appointment_date = ?
              AND appointment_time = ?
              AND status != 'Cancelled'
        """, (doctor_id, appointment_date, appointment_time))

        if cursor.fetchone():
            return jsonify({
                "message": "This time slot is already booked for this doctor"
            }), 409

        cursor.execute("""
            INSERT INTO appointments
            (user_id, doctor_id, hospital_id, appointment_date,
             appointment_time, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id, doctor_id, hospital_id,
            appointment_date, appointment_time, "Booked"
        ))

        appointment_id = cursor.lastrowid
        connection.commit()

        return jsonify({
            "message": "Appointment booked successfully",
            "appointment_id": appointment_id
        }), 201

    except (ValueError, TypeError):
        return jsonify({"message": "Invalid user, doctor or hospital ID"}), 400
    except Exception:
        app.logger.exception("Appointment booking failed")
        return jsonify({"message": "Could not book appointment"}), 500
    finally:
        if connection is not None:
            connection.close()


# =========================
# PATIENT APPOINTMENT HISTORY
# =========================

@app.route("/appointments/<int:user_id>", methods=["GET"])
def get_patient_appointments(user_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                appointments.id,
                appointments.user_id,
                appointments.doctor_id,
                appointments.hospital_id,
                appointments.appointment_date,
                appointments.appointment_time,
                appointments.status,
                doctors.name
            FROM appointments
            LEFT JOIN doctors
                ON appointments.doctor_id = doctors.id
            WHERE appointments.user_id = ?
            ORDER BY appointments.appointment_date, appointments.appointment_time
        """, (user_id,))
        rows = cursor.fetchall()

        return jsonify([
            {
                "id": row[0],
                "user_id": row[1],
                "doctor_id": row[2],
                "hospital_id": row[3],
                "appointment_date": row[4],
                "appointment_time": row[5],
                "status": row[6],
                "doctor_name": row[7],
            }
            for row in rows
        ]), 200
    except Exception:
        app.logger.exception("Appointment history retrieval failed")
        return jsonify({"message": "Could not retrieve appointments"}), 500
    finally:
        connection.close()


# =========================
# CANCEL APPOINTMENT
# =========================

@app.route("/appointments/<int:appointment_id>", methods=["DELETE"])
def cancel_appointment_api(appointment_id):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE appointments
            SET status = 'Cancelled'
            WHERE id = ? AND status != 'Cancelled'
        """, (appointment_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "message": "Appointment not found or already cancelled"
            }), 404

        return jsonify({
            "message": "Appointment cancelled successfully"
        }), 200
    except Exception:
        app.logger.exception("Appointment cancellation failed")
        return jsonify({"message": "Could not cancel appointment"}), 500
    finally:
        connection.close()


# =========================
# RESCHEDULE APPOINTMENT
# =========================

@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def reschedule_appointment_api(appointment_id):
    data = request.get_json(silent=True) or {}
    appointment_date = data.get("appointment_date")
    appointment_time = data.get("appointment_time")

    if not appointment_date or not appointment_time:
        return jsonify({
            "message": "Appointment date and time are required"
        }), 400

    allowed_slots = {
        "09:00", "10:00", "11:00", "14:00", "15:00",
        "16:00", "17:00", "18:00", "19:00", "20:00"
    }

    if appointment_time not in allowed_slots:
        return jsonify({"message": "Invalid appointment time slot"}), 400

    try:
        selected_date = datetime.strptime(
            appointment_date, "%Y-%m-%d"
        ).date()
    except ValueError:
        return jsonify({"message": "Invalid appointment date format"}), 400

    now = datetime.now()

    if selected_date < now.date():
        return jsonify({"message": "Cannot reschedule to a past date"}), 400

    if selected_date == now.date():
        selected_time = datetime.strptime(
            f"{appointment_date} {appointment_time}",
            "%Y-%m-%d %H:%M"
        )
        if selected_time <= now:
            return jsonify({
                "message": "This appointment time has already passed"
            }), 400

    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT doctor_id, status
            FROM appointments
            WHERE id = ?
        """, (appointment_id,))
        appointment = cursor.fetchone()

        if appointment is None:
            return jsonify({"message": "Appointment not found"}), 404

        doctor_id, status = appointment

        if status == "Cancelled":
            return jsonify({
                "message": "Cancelled appointments cannot be rescheduled"
            }), 400

        cursor.execute("""
            SELECT id FROM appointments
            WHERE doctor_id = ?
              AND appointment_date = ?
              AND appointment_time = ?
              AND id != ?
              AND status != 'Cancelled'
        """, (
            doctor_id, appointment_date, appointment_time, appointment_id
        ))

        if cursor.fetchone():
            return jsonify({
                "message": "This time slot is already booked for this doctor"
            }), 409

        cursor.execute("""
            UPDATE appointments
            SET appointment_date = ?,
                appointment_time = ?,
                status = 'Rescheduled'
            WHERE id = ?
        """, (appointment_date, appointment_time, appointment_id))

        connection.commit()
        return jsonify({
            "message": "Appointment rescheduled successfully"
        }), 200
    except Exception:
        app.logger.exception("Appointment rescheduling failed")
        return jsonify({"message": "Could not reschedule appointment"}), 500
    finally:
        connection.close()


# =========================
# SUBMIT FEEDBACK
# =========================

@app.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id", data.get("patient_id"))
    doctor_id = data.get("doctor_id")
    rating = data.get("rating")
    comment = data.get("comment", data.get("comments", ""))

    if user_id is None or doctor_id is None or rating is None:
        return jsonify({
            "message": "User ID, doctor ID and rating are required"
        }), 400

    try:
        user_id = int(user_id)
        doctor_id = int(doctor_id)
        rating = int(rating)

        if not 1 <= rating <= 5:
            return jsonify({"message": "Rating must be between 1 and 5"}), 400

        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if cursor.fetchone() is None:
                return jsonify({"message": "User not found"}), 404

            cursor.execute("SELECT id FROM doctors WHERE id = ?", (doctor_id,))
            if cursor.fetchone() is None:
                return jsonify({"message": "Doctor not found"}), 404
        finally:
            connection.close()

        add_feedback(user_id, doctor_id, rating, comment)

        return jsonify({"message": "Feedback submitted successfully"}), 201

    except (ValueError, TypeError):
        return jsonify({"message": "Invalid ID or rating"}), 400
    except Exception:
        app.logger.exception("Feedback submission failed")
        return jsonify({"message": "Could not submit feedback"}), 500


# =========================
# DOCTOR FEEDBACK
# =========================

@app.route("/feedback/doctor/<int:doctor_id>", methods=["GET"])
def doctor_feedback(doctor_id):
    try:
        rows = get_doctor_feedback(doctor_id)

        return jsonify([
            {
                "id": row[0],
                "user_id": row[1],
                "doctor_id": row[2],
                "rating": row[3],
                "comment": row[4],
                "created_at": row[5],
                "user_name": row[6],
            }
            for row in rows
        ]), 200
    except Exception:
        app.logger.exception("Doctor feedback retrieval failed")
        return jsonify({"message": "Could not retrieve feedback"}), 500


# =========================
# AI SYMPTOM SUMMARY
# =========================

@app.route("/symptom-summary", methods=["POST"])
def symptom_summary():
    import re

    try:
        data = request.get_json(silent=True) or {}
        symptoms = data.get("symptoms", "").strip()

        if not symptoms:
            return jsonify({
                "message": "Symptoms are required"
            }), 400

        summary = ""

        # Try Gemini first
        if gemini_client is not None:
            prompt = f"""
Extract only the key symptoms from the patient's description.

Rules:
- Return a short, comma-separated list.
- Include symptom duration when mentioned.
- Remove conversational wording and repetition.
- Do not repeat the full description.
- Do not diagnose or recommend treatment.
- Do not add symptoms that the patient did not report.

Example:
Input: I have fever for five days, a cold, and my
throat hurts when I swallow.
Output: Fever for 5 days, cold, sore throat,
pain while swallowing.

Patient description:
{symptoms}
"""

            try:
                response = gemini_client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                summary = (response.text or "").strip()

            except Exception as ai_error:
                app.logger.warning(
                    "Gemini unavailable; using local extraction: %s",
                    ai_error
                )

        # Local fallback if Gemini fails or returns no text
        if not summary:
            text = symptoms.lower()
            extracted = []

            patterns = [
                (
                    r"\bfever\b",
                    "Fever"
                ),
                (
                    r"\bcold\b",
                    "Cold"
                ),
                (
                    r"\bsore throat\b|\bthroat pain\b|\bthroat hurts\b",
                    "Sore throat"
                ),
                (
                    r"\bpain while swallowing\b|\bpain when i swallow\b"
                    r"|\bwhen i swallow\b|\bwhen i swallow anything\b",
                    "Pain while swallowing"
                ),
                (
                    r"\bcough\b",
                    "Cough"
                ),
                (
                    r"\bheadache\b",
                    "Headache"
                ),
                (
                    r"\bfatigue\b|\btiredness\b",
                    "Fatigue"
                ),
                (
                    r"\bbody aches?\b|\bbody pain\b",
                    "Body aches"
                ),
                (
                    r"\bnausea\b",
                    "Nausea"
                ),
                (
                    r"\bvomiting\b",
                    "Vomiting"
                ),
                (
                    r"\bdiarrhea\b",
                    "Diarrhea"
                ),
                (
                    r"\bshortness of breath\b|\bdifficulty breathing\b",
                    "Shortness of breath"
                ),
            ]

            for pattern, label in patterns:
                if re.search(pattern, text) and label not in extracted:
                    extracted.append(label)

            # Preserve fever duration when stated
            fever_duration = re.search(
                r"\bfever\b.{0,40}?"
                r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
                r"\s+days?\b"
                r"|\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)"
                r"\s+days?\b.{0,30}?\bfever\b",
                text
            )

            if "Fever" in extracted and fever_duration:
                raw_duration = (
                    fever_duration.group(1) or fever_duration.group(2)
                )

                number_words = {
                    "one": "1",
                    "two": "2",
                    "three": "3",
                    "four": "4",
                    "five": "5",
                    "six": "6",
                    "seven": "7",
                    "eight": "8",
                    "nine": "9",
                    "ten": "10",
                }

                days = number_words.get(raw_duration, raw_duration)
                extracted[extracted.index("Fever")] = (
                    f"Fever for {days} days"
                )

            if extracted:
                summary = ", ".join(extracted)
            else:
                summary = (
                    "Could not identify specific symptoms. "
                    "Please review the patient's original description."
                )

        print("AI SYMPTOM SUMMARY:", summary)

        return jsonify({
            "summary": summary
        }), 200

    except Exception:
        app.logger.exception("Symptom summary failed")

        return jsonify({
            "message": "Symptom summary generation failed"
        }), 500



# =========================
# START SERVER
# =========================

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)