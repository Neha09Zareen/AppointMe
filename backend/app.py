from flask import Flask, request, jsonify
from flask_cors import CORS
from database import create_tables, add_user, get_user_by_email, get_all_hospitals, add_doctor, get_all_doctors, get_connection

app = Flask(__name__)
CORS(app)

@app.route("/appointments/<int:appointment_id>/cancel", methods=["PUT"])
def cancel_appointment_route(appointment_id):
    cancel_appointment(appointment_id)

    return jsonify({
        "message": "Appointment cancelled successfully"
    })

@app.route("/")
def home():
    return "Welcome to AppointMe Backend!"

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
        "message": "Login Successful"
    })

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

    return jsonify({"error": "Doctor not found"}), 404

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

@app.route("/appointments/<int:patient_id>", methods=["GET"])
def get_patient_appointments(patient_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, patient_id, doctor_id,
               appointment_date, appointment_time, status
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

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
