import json, requests
from database.models import Image, Message, Listing
from database.database import db
from sqlalchemy import or_
from flask import Blueprint, jsonify, url_for, redirect, render_template, request
from flask_login import login_required, logout_user, current_user

private_view = Blueprint("private_view", __name__)

""" These endpoints / views require user login. """

@private_view.route('/logout')
@login_required
def logout():
    logout_user()
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
    if current_user.id != message_history[-1]['id']:
        if message.unread:
            message.unread = False
        else:
            message.unread = True
        db.session.commit()
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

@private_view.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('account.html', user=current_user)

@private_view.route('/preview_listing/<int:listing_id>', methods=['GET'])
@login_required
def preview_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing or current_user.id is not listing.user_id:
        return jsonify(message='Access to listing is not allowed!'),400
    return render_template("preview_listing.html", user=current_user, listing=listing)

@private_view.route('/edit_listing/<int:listing_id>', methods=['GET'])
@login_required
def edit_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing or current_user.id is not listing.user_id:
        return redirect(url_for('private_view.profile'))
    return render_template("edit_listing.html", user=current_user, listing=listing)

@private_view.route('/delete_listing/<int:listing_id>', methods=["DELETE"])
@login_required
def listing_delete(listing_id):
    delete_request = requests.delete(url=f'{request.root_url}{url_for("listing.delete_listing")}',
                                     json={'listing_id':listing_id,'user_id': current_user.id})
    if delete_request.ok:
        return jsonify(message="Listing Deleted!"),200
    return jsonify(message="Listing could not be deleted!"),400

@private_view.route('/update_listing/<int:listing_id>', methods=['PUT'])
@login_required
def listing_update(listing_id):
    data = request.json
    for key in ('title','description','price'):
        if key not in data:
            return jsonify(message=f'{key} is missing from JSON'),400

    payload = {
        'title': data['title'],
        'description': data['description'],
        'price': data['price'],
        'user_id': current_user.id,
        'listing_id': listing_id,
        'images': data['images']
    }

    response = requests.put(url=f'{request.root_url}{url_for("listing.update_listing")}', json=payload)
    if response.ok:
        return jsonify(message="Listing Updated!"),200
    elif response.status_code == 401:
        return jsonify(message='Invalid file type, only [.png, .jpg, .jpeg, and .gif] are allowed!'),401
    return jsonify(message="Listing Could Not Be Updated!"),400

