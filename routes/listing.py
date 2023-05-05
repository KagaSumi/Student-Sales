from database.database import db
from database.models import User,Listing
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, jsonify, request, flash, url_for, redirect, render_template
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime as DT

listing = Blueprint('listing', __name__)

@listing.route('/get_listing/<string:listing_id>',methods=['GET'])
def get_listing(listing_id):
    listing = Listing.query.get(listing_id)
    if not listing:
            return jsonify(message=ValueError.message),404
    return jsonify(message=listing.to_dict()),200
    
@listing.route('/create_listing_new',methods=['POST'])
def create_listing():
    data = request.json
    for key in ("title","description","price","user_id"):
        if key not in data:
            return f"The JSON provided is invalid (missing: {key})", 400
    try:
        title = str(data["title"])
        description = str(data["description"])
        price = round(float(data["price"]),2)
        user_id = data["user_id"]
        if not User.query.get(user_id):
            raise ValueError(f"The user {user_id} does not exist")
        if price < 0:
           raise ValueError("The price cannot be negative")
    except ValueError as err:
            return (f"Error: {str(err)}!",400)
    listing = Listing(title=title, description=description, 
                      price=price, user_id=user_id)
    db.session.add(listing)
    db.session.commit()
    return jsonify(message='New Listing Added'), 200

@listing.route('/update_listing/<string:listing_id>',methods=['PUT'])
def update_listing(listing_id):
    data = request.json
    listing = Listing.query.get(listing_id)
    if not listing:
        return jsonify(message="Listing Does not Exist"),404
    for key in ("title","description","price","user_id"):
        if key not in data:
            return f"The JSON provided is invalid (missing: {key})", 400
    try:
        title = str(data["title"])
        description = str(data["description"])
        price = round(float(data["price"]),2)
        if not User.query.get(data["user_id"]):
            raise ValueError("The user does not exist")
        if price < 0:
           raise ValueError("The price cannot be negative")
        if listing.user_id != data["user_id"]:
            raise ValueError("The user does not own this listing")
    except ValueError as err:
            return (f"Error: {str(err)}!",400)
    listing.title = title
    listing.description = description
    listing.price = price
    db.session.commit()
    return jsonify(message='Listing Updated'), 200

@listing.route('/delete_listing/<string:listing_id>',methods=['DELETE'])
def delete_listing(listing_id):
    data = request.json
    if not data.get("user_id"):
        return jsonify("User does not exist"),400
    listing = Listing.query.get(listing_id)
    if listing.user_id != data["user_id"]:
        return jsonify("User does not own the listing"),400
    db.session.delete(listing)
    db.session.commit()
    return jsonify(message='User Deleted'), 200
