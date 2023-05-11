from database.database import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    is_confirmed = db.Column(db.Boolean, default=False)
    listings = db.relationship('Listing',cascade="all,delete" ,backref='user')
    def __str__(self):
        return f'<User(id="{self.id}", email="{self.email}", first_name="{self.first_name}", last_name="{self.last_name}")>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
        
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    price = db.Column(db.Float)
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

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