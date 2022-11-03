import requests

from flask import Blueprint, request, jsonify

from settings import URL_ACADEMIC

subjects_bp = Blueprint("subjects_blueprint", __name__)


@subjects_bp.route("", methods=["GET"])
def get_all():
    response = requests.get(
        url=f"{URL_ACADEMIC}/subjects",
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


@subjects_bp.route("<string:id_subject>", methods=["GET"])
def get_by_id():
    ...


@subjects_bp.route("", methods=["POST"])
def create():
    ...


@subjects_bp.route("<string:id_subject>", methods=["PUT"])
def update():
    ...


@subjects_bp.route("<string:id_subject>", methods=["DELETE"])
def delete():
    ...
