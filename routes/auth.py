import requests
from database.database import db
from database.models import User
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, jsonify, request, url_for, redirect, render_template
from flask import current_app as app
from flask_mail import Message
from extensions import mail
from itsdangerous import URLSafeTimedSerializer

auth = Blueprint('auth', __name__)

""" These endpoints / views perform the logic for user management. """

# Email Verification Functions
def generate_token(email):
    serializer = URLSafeTimedSerializer('fdkjshfhjsdfdskfdsfdcbsjdkfdsdf')
    return serializer.dumps(email, salt="very-important")

def confirm_token(token):
    serializer = URLSafeTimedSerializer('fdkjshfhjsdfdskfdsfdcbsjdkfdsdf')
    try:
        email = serializer.loads(
            token, salt="very-important"
        )
        return email
    except Exception:
        return False

def send_email(to, subject, template):
    with app.app_context():
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender=app.config["MAIL_DEFAULT_SENDER"],
        )
        mail.send(msg)

@auth.route('/sign-up', methods=['POST'])
def register():
    data = request.json
    for key in ['email', 'password', 'first_name', 'last_name', 'phone_number']:
        if key not in data:
            return jsonify(message=f'{key} is missing from JSON'), 400
        
    if User.query.filter_by(email=data['email'].lower()).first():
        return jsonify(message='Email already registered with an account!'), 400
    payload = {
        'email': data['email'],
        'password': data['password'],
        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'phone_number': data['phone_number']
    }
    response = requests.post(url=f'{request.root_url}{url_for("user.create_user")}', json=payload)
    if response.ok:
        token = generate_token(data["email"])
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template("confirmation_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(data["email"], subject, html)
        return jsonify(message='A confirmation email has been sent!'), 200
    return jsonify(message='Incorrect Email or Password!'), 400

@auth.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    print(email)
    if not email:
        return redirect(url_for("public_view.homepage"))
    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        return redirect(url_for("public_view.homepage"))
    print(user)
    user.is_confirmed = True
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=False)
    return redirect(url_for("private_view.profile"))


@auth.route("/change_password",methods=["GET"])
@login_required
def view_forgot_password_logged_in():
    return render_template("forgot_password.html", user=current_user)

@auth.route('/change_password/<token>',methods=["GET"])
def view_forget_password(token):
    return render_template("forgot_password.html", user=None)

@auth.route('/change_password/',methods=["PUT"])
@login_required
def update_password():
    data = request.json
    if "password" not in data:
        return jsonify(message="password missing from JSON"),400
    user = current_user
    user.password = str(data['password'])
    db.session.commit()
    logout_user()
    return jsonify(message="Password updated successfully"),200

@auth.route('/change_password/<token>',methods=["PUT"])
def update_password_no_login(token):
    data = request.json
    if "password" not in data:
        return jsonify(message="password missing from JSON"),400
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first()
    user.password = str(data['password'])
    db.session.commit()
    logout_user()
    return jsonify(message="Password updated successfully"),200

@auth.route('/forgot_password',methods=["POST"])
def forget_password():
    data = request.json
    if "email" not in data:
        return jsonify(message="email missing from JSON"),400
    if User.query.filter_by(email=data["email"].lower()).first():
        token = generate_token(data["email"].lower())
        confirm_url = url_for("auth.view_forget_password", token=token, _external=True)
        html = render_template("reset_password_email.html", confirm_url=confirm_url)
        subject = "Password reset for Student Sales"
        send_email(data["email"],subject,html)
    return jsonify(message="Email Sent to Address if registered"),200 #redirect to login

@auth.route('/forgot_password',methods=["GET"])
def forgot_password():
    return render_template("forgot_password_email.html", user=None)


@auth.route('/update_profile', methods=['PUT'])
@login_required
def update_user():
    data = request.json
    for key in ['first_name', 'last_name','phone_number']:
        if key not in data:
            return jsonify(message=f"{key} is missing from JSON")
        
    update_request = requests.put(url=f'{request.host_url}{url_for("user.update_user", user_id=str(current_user.id))}',
        json={
        'first_name': data['first_name'], 
        'last_name': data['last_name'],
        'phone_number': data['phone_number'],
    })

    if update_request.ok:
        return jsonify(message='Account Updated!'),200
    
    return jsonify(message='Account Update Failed!'),400

@auth.route('/login', methods=['POST'])
def user_login():
    data = request.json
    for key in ['email', 'password']:
        if key not in data:
            return jsonify(message=f'{key} is missing from JSON'),400
    payload = {
        'email': data['email'],
        'password': data['password']
        }
    response = requests.post(url=f'{request.root_url}{url_for("user.verify_user")}', json=payload)
    if response.ok:
        user = User.query.filter_by(email=data['email']).first()
        login_user(user, remember=False)
        return jsonify(message='Login Successful!'), 200
    if response.status_code == 401:
        return jsonify(message='Please verify your email!'),400
    return jsonify(message='Incorrect Email or Password!'), 400

@auth.route('/delete_user', methods=["DELETE"])
@login_required
def delete_user():
    delete_request = requests.delete(f'{request.root_url}{url_for("user.delete_user",user_id=int(current_user.id))}') 
    if delete_request.ok:
        logout_user()
        return jsonify(message='User Deleted'),200
    return jsonify(message='Failed to delete user'),400

@auth.route('/create_listing', methods=['POST'])
@login_required
def listing_create():
    data = request.json

    for key in ['title', 'description', 'price']:
        if key not in data:
            return jsonify(message=f'{key} is missing from JSON'), 400
    
    payload = {
        'title': data['title'],
        'description': data['description'],
        'price': data['price'],
        'user_id': current_user.id,
        'images': data['images']
    }

    response = requests.post(f'{request.root_url}{url_for("listing.create_listing")}', json=payload)
    if response.ok or response.status_code == 500:
        return jsonify(message='Listing Created!'), 200
    elif response.status_code == 401:
        return jsonify(message='Invalid file type, only [.png, .jpg, .jpeg, and .gif] are allowed!'),401
    return jsonify(message='Error Occurred in Creating Listing!'), 400

@ auth.app_errorhandler(404)
def page_not_found(err):
    return render_template('404.html', user=current_user), 404
