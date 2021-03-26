from . import db
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    marks = db.relationship('Marks')


class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tenthmarks = db.Column(db.String(50))
    intermarks = db.Column(db.String(50))
    degreemarks = db.Column(db.String(50))
