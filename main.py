import datetime

from flask import Flask, jsonify, request
from settings import URL, PORT, URL_SECURITY, JWT_SECRET_KEY, URL_ACADEMIC
import requests
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)


@app.route("/", methods=["GET"])
def ping():
    return jsonify({
        "message": "pong..."
    })


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(
        url=f"{URL_SECURITY}/users/auth",
        json=body,
        headers=headers
    )

    if response.status_code == 200:
        user = response.json()
        expire = datetime.timedelta(hours=24)  # 1 dia de vencimiento
        access_token = create_access_token(
            identity=user,
            expires_delta=expire
        )
        return jsonify({
            "token": access_token,
        })
    else:
        return jsonify({
            "message": "Bad username or password"
        }), 400


@app.route("/students", methods=["GET"])
def get_all_students():
    if verify_jwt_in_request():
        response = requests.get(
            url=f"{URL_ACADEMIC}/students",
            headers={
                "Content-Type": "application/json"
            }
        )
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                "students": data.get("students", [])
            })
        else:
            return jsonify({
                "message": "error"
            }), 400
    else:
        return jsonify({
            "message": "not auth"
        }), 401


@app.route("/departments", methods=["GET"])
def get_all_departments():
    # middleware -> la solución  para proteger las rutas sin repetir codigo...!
    if verify_jwt_in_request():
        response = requests.get(
            url=f"{URL_ACADEMIC}/departments",
            headers={
                "Content-Type": "application/json"
            }
        )

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "messags": "se presento un error"
            })


if __name__ == "__main__":
    app.run(
        host=URL,
        port=PORT,
        debug=True
    )
