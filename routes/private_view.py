import json
from database.models import Image, Message
from database.database import db
from sqlalchemy import or_
from flask import Blueprint, jsonify,flash, url_for, redirect, render_template, request
from flask_login import login_required, logout_user, current_user

private_view = Blueprint("private_view", __name__)

""" These endpoints / views require user login. """

@private_view.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out Successfully!', 'success')
    return redirect(url_for('public_view.login'))

@private_view.route('/create_listing', methods=['GET'])
@login_required
def create_listing():
    return render_template('create_listing.html', user=current_user)

@private_view.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@private_view.route('/messages')
@login_required
def messages():
    messages = Message.query.filter(or_(Message.buyer_id == current_user.id, Message.seller_id == current_user.id)).all()
    return render_template('messages.html', user=current_user, messages=messages)

@private_view.route('/view_message/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get(message_id)
    message_history = json.loads(message.message)
    return render_template('view_message.html', user=current_user, message=message, message_history=message_history)

@private_view.route('/image/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    try:
        image = Image.query.get(image_id)
        db.session.delete(image)
        db.session.commit()
        return jsonify(message='Image Deleted!'),200
    except:
        return jsonify(message='Image Could Not Be Deleted!'),400
    
