import base64
from database.database import db
from flask_login import current_user
from database.models import Image, Listing
from flask import Blueprint, Response, jsonify, request, url_for, redirect, render_template
from sqlalchemy import or_

public_view = Blueprint('public_view', __name__)

""" These endpoints / views do not require user login. """

@public_view.route('/')
def homepage():
    return render_template('homepage.html', user=current_user)

@public_view.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.account'))
    
    return render_template('login.html', user=current_user)

@ public_view.route('/sign-up', methods=['GET'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.account'))
    
    return render_template('sign_up.html', user=current_user)

@public_view.route('/image/<int:image_id>')
def get_image(image_id):
    img = Image.query.get(image_id)
    image_data = img.img.split(',')[1]
    return Response(base64.b64decode(image_data),mimetype=img.mimetype)

@public_view.route('/view_listing/<int:listing_id>', methods=['GET'])
def view_listing(listing_id):
    listing = db.session.get(Listing, listing_id)
    if not listing: 
        return jsonify(message='Listing not found for viewing!'), 404
    return render_template('view_listing.html', user=current_user, listing=listing)

@public_view.route('/search')
def search():
    query = request.args.get('query')
    if query.isdigit():
        listings = Listing.query.filter(Listing.id == int(query)).all()
    else:
        listings = Listing.query.filter(Listing.title.contains(query)).all()
    return render_template('search_results.html', user=current_user, listings=listings, query=query)


@public_view.route('/search_api', methods=['GET'])
def search_api():
    query = request.args.get('query', '')
    if query.isdigit():
        listings = Listing.query.filter(Listing.id == int(query)).all()
    else:
        listings = Listing.query.filter(db.func.lower(Listing.title).contains(query.lower())).all()
    return jsonify([listing.to_dict() for listing in listings])




