import requests

from flask import Blueprint, request, jsonify

from settings import URL_ACADEMIC, URL_SECURITY

students_bp = Blueprint("students_blueprint", __name__)


@students_bp.before_request
def middleware_students():
    print("middleware_students...")


@students_bp.route("", methods=["GET"])
def get_all():
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


@students_bp.route("<string:id_student>", methods=["GET"])
def get_by_id(id_student):
    response = requests.get(
        url=f"{URL_ACADEMIC}/students/{id_student}",
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


@students_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    # 1. Crear el estudiante
    response = requests.request(
        method="POST",
        url=f"{URL_ACADEMIC}/students",
        json={
            "cedula": body["cedula"],
            "email": body["email"],
            "first_name": body["first_name"],
            "last_name": body["last_name"],
        },
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 201:
        # 2.1 Asignar el rol al usuario
        # 2.1.1 Consultar los roles
        roles_response = requests.request(
            method="GET",
            url=f"{URL_SECURITY}/role",
            headers={
                "Content-Type": "application/json"
            }
        )
        roles = roles_response.json() if roles_response.status_code == 200 else []
        student_role = None
        for role in roles:
            if role["name"] == "Estudiante":
                student_role = role
                break
        student = response.json()["student"]
        if student_role:
            user_response = requests.request(
                method="POST",
                url=f"{URL_SECURITY}/users?idRole={student_role['_id']}",
                json={
                    "username": body["username"],
                    "email": body["email"],
                    "password": body["password"]
                },
                headers={
                    "Content-Type": "application/json"
                }
            )
        else:
            user_response = requests.request(
                method="POST",
                url=f"{URL_SECURITY}/users",
                json={
                    "username": body["username"],
                    "email": body["email"],
                    "password": body["password"]
                },
                headers={
                    "Content-Type": "application/json"
                }
            )
        if user_response.status_code < 300:
            user = user_response.json()
            # 3. Asignar el usuario al estudiante
            assign_response = requests.request(
                method="PUT",
                url=f"{URL_ACADEMIC}/students/{student['_id']}/auth/{user['_id']}",
                headers={
                    "Content-Type": "application/json"
                }
            )
            if assign_response.status_code == 200:
                return jsonify(assign_response.json()), 201

    return jsonify({
        "msg": "Error"
    }), 400


@students_bp.route("<string:id_student>", methods=["PUT"])
def update(id_student):
    # URL_ACADEMIC + "/students/" + id_student es igual a f"{URL_ACADEMIC}/students/{id_student}"
    body = request.get_json()
    response = requests.request(
        method="PUT",
        url=f"{URL_ACADEMIC}/students/{id_student}",
        json=body,
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "Error"
        }), 400


@students_bp.route("<string:id_student>", methods=["DELETE"])
def delete(id_student):
    response_registrations = requests.request(
        method="DELETE",
        url=f"{URL_ACADEMIC}/students/{id_student}/delete-registrations",
        headers={
            "Content-Type": "application/json"
        }
    )
    response_student = requests.request(
        method="GET",
        url=f"{URL_ACADEMIC}/students/{id_student}",
        headers={
            "Content-Type": "application/json"
        }
    )
    if response_student.status_code == 200:
        student = response_student.json()
        if student.get("auth_id"):
            requests.request(
                method="DELETE",
                url=f"{URL_SECURITY}/users/{student['auth_id']}",
                headers={
                    "Content-Type": "application/json"
                }
            )
    if response_registrations.status_code == 200:
        response = requests.request(
            method="DELETE",
            url=f"{URL_ACADEMIC}/students/{id_student}",
            headers={
                "Content-Type": "application/json"
            }
        )
        if response.status_code == 200:
            return jsonify({
                "msg": f"el estudiante con id: {id_student} fue borrado",
                "registrations": response_registrations.json()
            })

    return jsonify({
        "msg": "error"
    }), 400
