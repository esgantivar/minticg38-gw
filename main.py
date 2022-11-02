import datetime
import bson
from flask import Flask, jsonify, request
from settings import URL, PORT, URL_SECURITY, JWT_SECRET_KEY, URL_ACADEMIC
import requests
from flask_jwt_extended import JWTManager, create_access_token, verify_jwt_in_request, get_jwt_identity

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


@app.route("/students/<string:user_id>", methods=["GET"])
def get_student_by_id(user_id):
    response = requests.get(
        url=f"{URL_ACADEMIC}/students/{user_id}",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({
            "message": "error"
        }), 400


@app.route("/departments", methods=["GET"])
def get_all_departments():
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


EXCLUDED_URLS = [
    "/",
    "/login"
]


def clean_path(path):
    parts = path.split("/")
    for idx, part in enumerate(parts):
        if bson.ObjectId.is_valid(part):
            parts[idx] = '?'
    return "/".join(parts)


def validate_permission(role_id, url, method) -> bool:
    """
    :return: si tiene permiso de acceso al recurso
    """
    response = requests.post(
        f"{URL_SECURITY}/role-permission/validate/role/{role_id}",
        json={
            "url": url,
            "method": method
        }
    )
    return response.status_code == 200


@app.before_request
def middleware():
    if request.path not in EXCLUDED_URLS:
        if verify_jwt_in_request():
            user = get_jwt_identity()
            role = user.get("role")
            role_id = role.get("_id")
            if not validate_permission(role_id, clean_path(request.path), request.method):
                return jsonify({
                    "msg": "Recurso no autorizado"
                }), 403


if __name__ == "__main__":
    app.run(
        host=URL,
        port=PORT,
        debug=True
    )
