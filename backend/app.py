from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    create_tables,
    add_user,
    get_user_by_email,
    get_all_hospitals,
    get_all_doctors,
    get_connection
)

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Welcome to AppointMe Backend!"


# REGISTER
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

        # Get the newly registered user's ID
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


# LOGIN
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


# HOSPITALS
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


# DOCTORS
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


# BOOK APPOINTMENT
@app.route("/appointments", methods=["POST"])
def book_appointment():
    data = request.get_json()

    patient_id = data["patient_id"]
    doctor_id = data["doctor_id"]
    appointment_date = data["appointment_date"]
    appointment_time = data["appointment_time"]

    connection = get_connection()
    cursor = connection.cursor()

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


# CANCEL APPOINTMENT
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


# RESCHEDULE APPOINTMENT
@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def reschedule_appointment(appointment_id):
    data = request.get_json()

    appointment_date = data["appointment_date"]
    appointment_time = data["appointment_time"]

    connection = get_connection()
    cursor = connection.cursor()

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

    if cursor.rowcount == 0:
        connection.close()

        return jsonify({
            "message": "Appointment not found"
        }), 404

    connection.close()

    return jsonify({
        "message": "Appointment rescheduled successfully"
    })


# PATIENT APPOINTMENTS
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


# DOCTOR APPOINTMENTS
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


# SUBMIT FEEDBACK
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


# ADMIN STATISTICS
@app.route("/admin-stats", methods=["GET"])
def get_admin_stats():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM doctors")
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


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)