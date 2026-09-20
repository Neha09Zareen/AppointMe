from flask import Flask, request, jsonify
from flask_cors import CORS

from database import (
    create_tables,
    get_connection,
    get_all_users,
    add_user,
    get_user_by_email,
    get_all_hospitals,
    get_all_doctors,
    get_all_appointments,
    cancel_appointment,
    add_feedback,
    get_doctor_feedback,
    get_doctor_appointments
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
# REGISTER
# =========================

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    add_user(
        data["name"],
        data["email"],
        data["password"],
        data["phone"]
    )

    return jsonify({
        "message": "Registration Successful"
    })


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = get_user_by_email(data["email"])

    if user is None:
        return jsonify({
            "message": "User not found"
        }), 404

    if user[3] != data["password"]:
        return jsonify({
            "message": "Incorrect password"
        }), 401

    return jsonify({
        "message": "Login Successful",
        "user_id": user[0],
        "name": user[1],
        "email": user[2]
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
# ALL DOCTORS
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


# =========================
# SINGLE DOCTOR
# =========================

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


# =====================================================
# BOOK APPOINTMENT
# =====================================================

@app.route("/appointments", methods=["POST"])
def book_appointment_route():

    try:

        data = request.get_json()

        print("BOOKING DATA RECEIVED:", data)

        # Your frontend currently sends user_id.
        # Your database uses patient_id.
        #
        # So we accept either one.

        patient_id = data.get("patient_id")

        if patient_id is None:
            patient_id = data.get("user_id")

        doctor_id = data.get("doctor_id")
        appointment_date = data.get("appointment_date")
        appointment_time = data.get("appointment_time")

        # hospital_id is intentionally NOT inserted.
        # Your appointments table does not contain hospital_id.

        if patient_id is None:
            return jsonify({
                "message": "Patient/User ID is required"
            }), 400

        if doctor_id is None:
            return jsonify({
                "message": "Doctor ID is required"
            }), 400

        if not appointment_date:
            return jsonify({
                "message": "Appointment date is required"
            }), 400

        if not appointment_time:
            return jsonify({
                "message": "Appointment time is required"
            }), 400

        connection = get_connection()
        cursor = connection.cursor()

        # IMPORTANT:
        # Your actual appointments table is:
        #
        # id
        # patient_id
        # doctor_id
        # appointment_date
        # appointment_time
        # status

        cursor.execute("""
            INSERT INTO appointments
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                status
            )
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

        print("APPOINTMENT BOOKED SUCCESSFULLY")

        return jsonify({
            "message": "Appointment booked successfully"
        }), 201

    except Exception as error:

        print("BOOKING ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =====================================================
# GET PATIENT APPOINTMENTS
# =====================================================

@app.route("/appointments/<int:user_id>", methods=["GET"])
def get_patient_appointments(user_id):

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # Database uses patient_id, NOT user_id

        cursor.execute("""
            SELECT
                id,
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                status
            FROM appointments
            WHERE patient_id = ?
            ORDER BY appointment_date, appointment_time
        """, (user_id,))

        appointments = cursor.fetchall()

        connection.close()

        return jsonify([
            {
                "id": appointment[0],
                "user_id": appointment[1],
                "patient_id": appointment[1],
                "doctor_id": appointment[2],
                "appointment_date": appointment[3],
                "appointment_time": appointment[4],
                "status": appointment[5]
            }
            for appointment in appointments
        ])

    except Exception as error:

        print("APPOINTMENT HISTORY ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =====================================================
# CANCEL APPOINTMENT
# =====================================================

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
        })

    except Exception as error:

        print("CANCEL ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =====================================================
# RESCHEDULE APPOINTMENT
# =====================================================

@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def reschedule_appointment_api(appointment_id):

    try:

        data = request.get_json()

        appointment_date = data.get("appointment_date")
        appointment_time = data.get("appointment_time")

        if not appointment_date or not appointment_time:

            return jsonify({
                "message": "Appointment date and time are required"
            }), 400

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE appointments
            SET
                appointment_date = ?,
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

        if cursor.rowcount == 0:

            connection.close()

            return jsonify({
                "message": "Appointment not found"
            }), 404

        connection.close()

        return jsonify({
            "message": "Appointment rescheduled successfully"
        })

    except Exception as error:

        print("RESCHEDULE ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =====================================================
# FEEDBACK
# =====================================================

@app.route("/feedback", methods=["POST"])
def submit_feedback():

    try:

        data = request.get_json()

        user_id = data.get("user_id")
        doctor_id = data.get("doctor_id")
        rating = data.get("rating")
        comment = data.get("comment")

        if not user_id or not doctor_id or not rating:

            return jsonify({
                "message": "User, doctor and rating are required"
            }), 400

        if rating < 1 or rating > 5:

            return jsonify({
                "message": "Rating must be between 1 and 5"
            }), 400

        add_feedback(
            user_id,
            doctor_id,
            rating,
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


# =====================================================
# DOCTOR FEEDBACK
# =====================================================

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


# =====================================================
# DOCTOR APPOINTMENTS
# =====================================================

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


# =====================================================
# ADMIN USERS
# =====================================================

@app.route("/admin/users", methods=["GET"])
def admin_users():

    try:

        users = get_all_users()

        return jsonify([
            {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "phone": user[4]
            }
            for user in users
        ])

    except Exception as error:

        print("ADMIN USERS ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =====================================================
# ADMIN APPOINTMENTS
# =====================================================

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
        ])

    except Exception as error:

        print("ADMIN APPOINTMENTS ERROR:", error)

        return jsonify({
            "message": str(error)
        }), 500


# =====================================================
# START SERVER
# =====================================================

if __name__ == "__main__":

    create_tables()

    app.run(
        debug=True
    )