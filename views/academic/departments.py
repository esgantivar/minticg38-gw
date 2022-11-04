import requests

from flask import Blueprint, request, jsonify

from settings import URL_ACADEMIC

department_bp = Blueprint("department_blueprint", __name__)


@department_bp.route("", methods=["GET"])
def get_all():
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
            "msg": "se presento un error"
        }), 400


@department_bp.route("<string:id_department>", methods=["GET"])
def get_by_id(id_department):
    response = requests.get(
        url=f"{URL_ACADEMIC}/departments/{id_department}",
        headers={
            "Content-Type": "application/json"
        }
    )

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "messags": "se presento un error"
        }), 400


@department_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    response = requests.request(
        method="POST",
        url=f"{URL_ACADEMIC}/departments",
        json=body,
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 201:
        return jsonify(response.json()), 201
    else:
        return jsonify({
            "msg": "error"
        }), 400


@department_bp.route("<string:id_department>", methods=["PUT"])
def update(id_department):
    body = request.get_json()
    response = requests.request(
        method="PUT",
        url=f"{URL_ACADEMIC}/departments/{id_department}",
        json=body,
        headers={
            "Content-Type": "application/json"
        }
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "error"
        }), 400


@department_bp.route("<string:id_department>", methods=["DELETE"])
def delete(id_department):
    response = requests.request(
        method="DELETE",
        url=f"{URL_ACADEMIC}/departments/{id_department}",
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "error"
        }), 400
