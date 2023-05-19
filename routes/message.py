import json
from database.database import db
from flask_login import current_user, login_required
from flask import Blueprint, jsonify, request
from database.models import Message, Listing

message = Blueprint('message', __name__)

@message.route("/create_message", methods=["POST"])
def create_message():
    if not current_user.is_authenticated:
        return jsonify(message='You must be logged in to send messages!'), 400
    
    data = request.json
    for key in ('subject', 'message', 'listing_id'):
        if key not in data:
            return jsonify(message=f'{key} is missing from JSON'), 400
        if data[key] == '':
            return jsonify(message='Please fill in both the subject and message fields!'), 400

    listing = Listing.query.get(data['listing_id'])

    if listing.user_id == current_user.id:
        return jsonify(message='Cannot send message to your own listing!'), 400
    
    messages = Message.query.filter_by(listing_id=listing.id, buyer_id=current_user.id).all() 
    if messages:
        return jsonify(message='You have already replied to this listing!'), 400

    data['message'] = json.dumps([{'id' : current_user.id, 'message': data['message']}])
    new_message = Message(
        buyer_id = current_user.id,
        listing_id = listing.id,
        seller_id = listing.user_id,
        subject = data['subject'],
        message = data['message']
    )

    db.session.add(new_message)
    db.session.commit()
    return jsonify(message='Message has been sent!'), 200

@message.route("/update_message/<int:message_id>", methods=["PUT"])
def update_message(message_id):
    data = request.json
    if data['message'] == '':
        return jsonify(message='Please type something to send reply!'), 400

    message = Message.query.get(message_id)
    message_history = json.loads(message.message)
    new_message = {'id' : current_user.id, 'message': data['message']}
    message_history.append(new_message)
    message.unread = True
    message.message = json.dumps(message_history)
    db.session.commit()

    return jsonify(message='Reply Sent!'), 200