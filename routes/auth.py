from flask import Blueprint, request, flash, url_for, redirect, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def login():
    return render_template("login.html")
