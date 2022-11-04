import requests

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from settings import URL_ACADEMIC

HEADERS = {
    "Content-Type": "application/json"
}

myself_bp = Blueprint("myself_blueprint", __name__)


def _get_student():
    user = get_jwt_identity()
    auth_id = user.get("_id")
    response = requests.request(
        method="GET",
        url=f"{URL_ACADEMIC}/students/auth/{auth_id}",
        headers=HEADERS
    )
    if response.status_code == 200:
        return response.json()
    else:
        return None


def _get_registration(student, registration_id):
    if not student:
        return {
            "registration": None,
            "errors": ["Student Does not exist"]
        }
    response = requests.request(
        method="GET",
        url=f"{URL_ACADEMIC}/registrations/student/{student['_id']}/registration/{registration_id}",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        return {
            "registration": response.json()
        }
    else:
        return {
            "registration": None,
            "errors": ["Registration Does not exist"]
        }


@myself_bp.route("", methods=["GET"])
def get_myself():
    student = _get_student()
    if student:
        return jsonify(student)
    else:
        return jsonify({
            "msg": "error"
        }), 404


@myself_bp.route("", methods=["PUT"])
def update_myself():
    student = _get_student()
    if student:
        response = requests.request(
            method="PUT",
            url=f"{URL_ACADEMIC}/students/{student['_id']}",
            json=request.get_json()
        )
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                "msg": "error"
            }), 400
    else:
        return jsonify({
            "msg": "error"
        }), 404


@myself_bp.route("registrations", methods=["POST"])
def create_registration():
    student = _get_student()
    subject = request.get_json()["subject"]

    if not student:
        return jsonify({
            "msg": "error"
        }), 400

    response = requests.request(
        method="POST",
        url=f"{URL_ACADEMIC}/registrations",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "year": 2022,
            "semester": "II",
            "grade": 0.0,
            "student": {
                "id": student["_id"]
            },
            "subject": {
                "id": subject
            }
        }
    )
    if response.status_code == 201:
        return jsonify({
            "msg": "realizo la inscripción de forma exitosa",
            "respuesta": response.json()
        })
    else:
        return jsonify({
            "msg": "error"
        }), 400


@myself_bp.route("registrations", methods=["GET"])
def get_registrations():
    student = _get_student()
    if not student:
        return jsonify({
            "msg": ""
        }), 400
    response = requests.request(
        method="GET",
        url=f"{URL_ACADEMIC}/registrations/student/{student['_id']}/registration",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": ""
        }), 400


@myself_bp.route("registrations/<string:registration_id>", methods=["GET"])
def get_registration_by_id(registration_id):
    response = _get_registration(registration_id)
    if response.get("registration"):
        return jsonify(response)
    else:
        return jsonify({
            "msg": ""
        }), 400


@myself_bp.route("registrations/<string:registration_id>", methods=["PUT"])
def update_registration(registration_id):
    body = request.get_json()
    student = _get_student()
    response = _get_registration(student, registration_id)
    subject = response.get("registration")
    if subject:
        res = requests.request(
            method="PUT",
            url=f"{URL_ACADEMIC}/registrations/{registration_id}",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "grade": subject["grade"],
                "semester": subject["semester"],
                "student": {
                    "id": student["_id"]
                },
                "subject": {
                    "id": body.get("subject")
                },
                "year": subject["year"]
            }
        )
        if res.status_code == 200:
            return jsonify(res.json())
    return jsonify({
        "msg": ""
    }), 400


@myself_bp.route("registrations/<string:registration_id>", methods=["DELETE"])
def delete_registration(registration_id):
    student = _get_student()
    response = _get_registration(student, registration_id)
    if response.get("registration"):
        res = requests.request(
            method="DELETE",
            url=f"{URL_ACADEMIC}/registrations/{registration_id}",
            headers={
                "Content-Type": "application/json"
            }
        )
        if res.status_code == 200:
            return jsonify(res.json())
    return jsonify({
        "msg": ""
    }), 400
