import requests

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from settings import URL_ACADEMIC

HEADERS = {
    "Content-Type": "application/json"
}

myself_bp = Blueprint("myself_blueprint", __name__)


def _get_student(auth_id):
    response = requests.request(
        method="GET",
        url=f"{URL_ACADEMIC}/students/auth/{auth_id}",
        headers=HEADERS
    )
    if response.status_code == 200:
        return response.json()
    else:
        return None


@myself_bp.route("", methods=["GET"])
def get_myself():
    user = get_jwt_identity()
    student = _get_student(user['_id'])
    if student:
        return jsonify(student)
    else:
        return jsonify({
            "msg": "error"
        }), 404


@myself_bp.route("", methods=["PUT"])
def update_myself():
    user = get_jwt_identity()
    student = _get_student(user['_id'])
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
    user = get_jwt_identity()
    student = _get_student(user["_id"])
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
    pass


@myself_bp.route("registrations/<string:registration_id>", methods=["GET"])
def get_registration_by_id(registration_id):
    user = get_jwt_identity()
    student = _get_student(user["_id"])
    if not student:
        return jsonify({
            "msg": ""
        }), 400
    response = requests.request(
        method="GET",
        url=f"{URL_ACADEMIC}/registrations/student/{student['_id']}/registration/{registration_id}",
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


@myself_bp.route("registrations/<string:registration_id>", methods=["PUT"])
def update_registration(registration_id):
    pass


@myself_bp.route("registrations/<string:registration_id>", methods=["DELETE"])
def delete_registration(registration_id):
    pass
