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
def get_by_id(id_subject):
    response = requests.get(
        url=f"{URL_ACADEMIC}/subjects/{id_subject}",
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


@subjects_bp.route("", methods=["POST"])
def create():
    body = request.get_json()
    response = requests.request(
        method="POST",
        url=f"{URL_ACADEMIC}/subjects",
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


@subjects_bp.route("<string:id_subject>", methods=["PUT"])
def update(id_subject):
    body = request.get_json()
    response = requests.request(
        method="PUT",
        url=f"{URL_ACADEMIC}/subjects/{id_subject}",
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


@subjects_bp.route("<string:id_subject>", methods=["DELETE"])
def delete(id_subject):
    response = requests.request(
        method="DELETE",
        url=f"{URL_ACADEMIC}/subjects/{id_subject}",
    )
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "msg": "error"
        }), 400
