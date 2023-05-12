from database.database import db
from database.models import User, Listing, Image
from flask import Blueprint, jsonify, request

listing = Blueprint("listing", __name__)

@listing.route("/get_listing/<int:listing_id>", methods=["GET"])
def get_listing(listing_id):
    requested_listing = Listing.query.get(listing_id)
    if not requested_listing:
        return jsonify(message="Listing does not exist"), 404
    return jsonify(message=requested_listing.to_dict()), 200

@listing.route("/create_listing_new", methods=["POST"])
def create_listing():
    data = request.json
    for key in ("title", "description", "price", "user_id"):
        if key not in data:
            return f"The JSON provided is invalid (missing: {key})", 400
    try:
        title = str(data["title"])
        description = str(data["description"])
        price = round(float(data["price"]), 2)
        user_id = data["user_id"]
        if not User.query.get(user_id):
            raise ValueError(f"The user {user_id} does not exist")
        if price < 0:
            raise ValueError("The price cannot be negative")
    except ValueError as err:
        return (f"Error: {str(err)}!", 400)
    
    new_listing = Listing(title=title, description=description, price=price, user_id=user_id)
    db.session.add(new_listing)
    db.session.commit()

    images = data['images']
    if images:
        for img in data['images']:
            image = Image(img=img['pic'],name=img['filename'],mimetype=img['mimetype'],listing=new_listing)
            db.session.add(image)
        db.session.commit()
    return jsonify(message="New Listing Added", listing=new_listing), 200

@listing.route('/update_listing', methods=['PUT'])
def update_listing():
    data = request.json
    listing = Listing.query.get(data['listing_id'])
    if not listing:
        return jsonify(message="Listing Does not Exist!"), 404
    for key in ("title", "description", "price", "user_id"):
        if key not in data:
            return f"The JSON provided is invalid (missing: {key})!", 400
    try:
        title = str(data["title"])
        description = str(data["description"])
        price = round(float(data["price"]), 2)
        if not User.query.get(data["user_id"]):
            raise ValueError("The user does not exist!")
        if price < 0:
            raise ValueError("The price cannot be negative!")
        if listing.user_id != data["user_id"]:
            raise ValueError("The user does not own this listing!")
    except ValueError as err:
        return (f"Error: {str(err)}!", 400)
    listing.title = title
    listing.description = description
    listing.price = price
    db.session.commit()
    return jsonify(message="Listing Updated!"), 200

@listing.route('/delete_listing', methods=['DELETE'])
def delete_listing():
    data = request.json
    if not data.get('user_id'):
        return jsonify('User does not exist!'), 400
    requested_listing = Listing.query.get(data['listing_id'])
    if requested_listing.user_id != data['user_id']:
        return jsonify('User does not own the listing!'), 400
    db.session.delete(requested_listing)
    db.session.commit()
    return jsonify(message='User Deleted'), 200
