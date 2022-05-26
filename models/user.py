from api.v1 import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.String(100), nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), unique=True)
    usage_count = db.Column(db.Integer, default=0)
    signup_date = db.Column(
        db.DateTime, default=datetime.utcnow()
    )  # this should have a default value.
    update_date = db.Column(db.DateTime)
    reviews = db.relationship("Review", backref="user", lazy=True)

    def to_dict(self):
        """Returns a dictionary containing a barber's information."""
        new_dict = self.__dict__.copy()

        if "password" in new_dict:
            new_dict.pop("password")

        new_dict.pop("_sa_instance_state")

        return new_dict

    def __repr__(self):
        return "<User %r>" % self.username
