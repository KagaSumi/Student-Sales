import json
from database.database import db
from flask_login import current_user
from flask import Blueprint, jsonify, request
from database.models import Message, Listing

message = Blueprint('message', __name__)

""" @message.route("/get_message/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return jsonify(message=user.to_dict()), 200
    return jsonify(message="User Not Found!"), 404 """

@message.route("/create_message", methods=["POST"])
def create_message():
    if not current_user.is_authenticated:
        return jsonify(message='You must be logged in to send messages!'), 400
    
    data = request.json
    for key in ('subject', 'message', 'listing_id'):
        if key not in data:
            return jsonify(message=f'{key} is missing from JSON'), 400

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