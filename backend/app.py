from flask import Flask, request, jsonify
from database import create_tables, add_user, get_user_by_email, get_all_hospitals, add_doctor, get_all_doctors

app = Flask(__name__)

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

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
