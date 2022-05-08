from app.v1.app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.String(100), nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), unique=True)
    usage_count = db.Column(db.Integer, default=0)
    signup_date = db.Column(db.DateTime, default=datetime.utcnow())  # this should have a default value.
    comments = db.relationship('Comments', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username
