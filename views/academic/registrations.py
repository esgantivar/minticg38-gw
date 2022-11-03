import requests

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from settings import URL_ACADEMIC

registrations_bp = Blueprint("registrations_blueprint", __name__)


@registrations_bp.route("", methods=["GET"])
def get_all():
    response = requests.get(
        url=f"{URL_ACADEMIC}/registrations",
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


@registrations_bp.route("<string:id_registration>", methods=["GET"])
def get_by_id(id_registration):
    response = requests.get(
        url=f"{URL_ACADEMIC}/registrations/{id_registration}",
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


@registrations_bp.route("", methods=["POST"])
def create():
    ...


@registrations_bp.route("<string:id_registration>", methods=["PUT"])
def update():
    ...


@registrations_bp.route("<string:id_registration>", methods=["DELETE"])
def delete():
    ...
