from database.database import db
from database.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, logout_user, current_user
import requests

public_view = Blueprint("public_view", __name__)


# This should be used for any pages that require the user to be logged in for


@public_view.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.account"))
    return render_template("login.html", user=current_user)
