from database.database import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    phone_number = db.Column(db.String)
    is_confirmed = db.Column(db.Boolean, default=False)
    listings = db.relationship('Listing', cascade="all,delete", backref='user')
    messages = db.relationship('Message', cascade="all,delete", backref='user')

    def __str__(self):
        return f'<User(id="{self.id}", email="{self.email}", first_name="{self.first_name}", last_name="{self.last_name}", phone_number="{self.phone_number}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number
        }
        
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float)
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    images = db.relationship('Image', cascade="all,delete", backref='listing')

    def __str__(self):
        return f'<Listing(id="{self.id}", title="{self.title}", description="{self.description}", price="{self.price}", date_posted="{self.date_posted}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'date_posted': self.date_posted,
            'user_id': self.user_id
        }
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False, index=True)

    def __str__(self):
        return f'<Image(id="{self.id}", name="{self.name}", mimetype="{self.mimetype}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'mimetype': self.mimetype,
            'listing_id': self.listing_id
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, nullable=False)
    listing_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    unread = db.Column(db.Boolean, default = True)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    def __str__(self):
        return f'<Message(id="{self.id}", seller_id="{self.seller_id}", listing_id="{self.listing_id}", buyer_id="{self.buyer_id}", subject="{self.subject}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'seller_id': self.seller_id,
            'listing_id': self.listing_id,
            'buyer_id': self.buyer_id,
            'subject': self.subject,
            'message': self.message,
            'unread': self.unread,
            'timestamp': self.timestamp
        }