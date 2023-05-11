from database.database import db
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, flash, url_for, redirect, render_template

user = Blueprint("user", __name__)


@user.route("/get_user/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(message=user.to_dict()), 200
    return jsonify(message="User Not Found"), 404


@user.route("/verify_user", methods=["POST"])
def verify_user():
    data = request.json
    for key in ("email", "password"):
        if key not in data:
            return jsonify(message=f"{key} is missing from JSON"), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not (user or check_password_hash(data["password"], user.password)):
        return jsonify(message=False), 400
    return jsonify(message=True), 200


@user.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    for key in ("email", "password", "first_name", "last_name", "phone_number"):
        if key not in data:
            return f"The JSON provided is invalid (missing: {key})", 400
    try:
        email = str(data["email"]).lower()
        password = str(data["password"])
        first_name = str(data["first_name"])
        last_name = str(data["last_name"])
        # phone_number = str(data["phone_number"])

        if "@" not in email:
            raise ValueError("Email is not valid")
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters")
    except ValueError as err:
        return (f"Error: {str(err)}!", 400)
    new_user = User(
        email=email,
        password=generate_password_hash(password, method="sha256"),
        first_name=first_name,
        last_name=last_name,
    )  # ,phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="New User Added"), 200


@user.route("/update_user/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    for key in ("email", "password", "first_name", "last_name", "phone_number"):
        if key not in data:
            return f"The JSON provided is invalid (missing: {key})", 400
    try:
        email = str(data["email"])
        password = str(data["password"])
        first_name = str(data["first_name"])
        last_name = str(data["last_name"])
        phone_number = str(data["phone_number"])

        if "@" not in email:
            raise ValueError("Email is not valid")
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters")
    except ValueError as err:
        return (f"Error: {str(err)}!", 400)
    user.email = email
    user.password = password
    user.first_name = first_name
    user.last_name = last_name
    user.phone_number = phone_number
    db.session.commit()
    return jsonify(message="User Updated"), 200


@user.route("/delete_user/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(message="User Deleted"), 200