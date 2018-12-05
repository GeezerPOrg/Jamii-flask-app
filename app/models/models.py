from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from datetime import date, datetime

class User(UserMixin, db.Model):
    """
    user model
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(60), unique = True)
    password_hash = db.Column(db.String(120))
    businesses = db.relationship('Businesses', backref = 'owner', lazy = True)
    reviews = db.relationship('Review', backref = 'review_owner', lazy = True)

    def __repr__(self):
        return f'{self.username}'

    #password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #checks whether password_hash is equal to password given
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Businesses(db.Model):
    """
    business table
    """
    __tablename__ = 'businesses'

    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())
    location = db.Column(db.String())
    started = db.Column(db.DateTime(), default = datetime.utcnow)
    business_description = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    reviews = db.relationship('Review', backref = 'business_review', lazy = True)



    def __repr__(self):
        return f'{self.name} is located at {self.location}'

class Review(db.Model):
    """
    table for reviews
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer(), primary_key = True)
    review_headline = db.Column(db.String(30))
    comment = db.Column(db.String())
    business_id = db.Column(db.Integer(), db.ForeignKey('businesses.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Title: {self.review_headline}, comment: {self.comment}>'
