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
            "messags": "se presento un error"
        })


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
        })


@department_bp.route("", methods=["POST"])
def create():
    ...


@department_bp.route("<string:id_department>", methods=["PUT"])
def update():
    ...


@department_bp.route("<string:id_department>", methods=["DELETE"])
def delete():
    ...
