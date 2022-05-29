#!/usr/bin/python3
"""Defines the classes (tables) Barber, BarberRating, and Styles."""
from email.policy import default
from api.v1 import db
from datetime import datetime
from models.ops import Review


# Define an associate table that associates IDs from
# the tables Barber_styles and Barbar.
barber_styles = db.Table(
    "barber_styles",
    db.Column(
        "barber_id", db.String(100), db.ForeignKey("barber.id"), primary_key=True
    ),
    db.Column("style_id", db.String(80), db.ForeignKey("style.id"), primary_key=True),
)


class Barber(db.Model):
    """Represents a Barber (table).
    
    Attributes:
        id (flask_sqlalchemy String): The Barber id.
        username (flask_sqlalchemy String): The unique username the Barber.
        firstname (flask_sqlalchemy String): The first name of the Barber.
        lastname (flask_sqlalchemy String): The last name of the Barber.
        email (flask_sqlalchemy String): The unique email address of the Barber
        phone (flask_sqlalchemy String): The unique phone number of the Barber.
        password (flask_sqlalchemy String): The password of the Barber.
        active (flask_sqlalchemy Integer): Defines if Barber is activated - 1,
            or deactivated - 0.
        country (flask_sqlalchemy String): The country of the Barber.
        state (flask_sqlalchemy String): The state of the Barber.
        city (flask_sqlalchemy String): The city of the Barber.
        address (flask_sqlalchemy String): The address of the Barber.
        signup_date (flask_sqlalchemy DateTime): The signup date of the Barber.
        updated_date (flask_sqlalchemy DateTime): The date the Barber model was updated.
        available (flask_sqlalchemy Boolean): Defines if the Barber is
            available to render service.
        job_count (flask_sqlalchemy Integer): The number of jobs the Barber has done.
        styles (List): A list of Hairstyle objects.
        reviews (List): A list of Review objects for the Barber.

    Example adding style to Barber list of styles:
        john = Barber(id='xxx', username='john')
        paul = Barber(id='xxx', username='paul')
        db.session.add_all([john, paul])
        db.session.commit()

        style1 = Style(name='punk')
        style2 = Style(name='afro')
        db.session.add_all([style1, style2])
        db.session.commit()

        # now we add a style for a barber
        john.styles.append(style1)
        db.session.commit()
    """

    id = db.Column(db.String(80), nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Integer) # activated == 1, deactivated == 0
    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.String(255))
    signup_date = db.Column(
        db.DateTime, default=datetime.utcnow()
    )  # this should have a default value.
    updated_date = db.Column(db.DateTime, default=datetime.utcnow())
    available = db.Column(db.Boolean, default=0)
    job_count = db.Column(db.Integer, default=0)
    styles = db.relationship(
        "Style",
        secondary=barber_styles,
        lazy="subquery",
        backref=db.backref("barbers", lazy=True),
    )
    reviews = db.relationship("Review", backref="barbers", lazy=True)

    def to_dict(self):
        """Returns a dictionary containing a barber's information."""
        new_dict = self.__dict__.copy()

        if "password" in new_dict:
            new_dict.pop("password")

        if self.styles:
            styles = [style.name for style in self.styles]
            new_dict["styles"] = styles

        new_dict.pop("_sa_instance_state")

        return new_dict

    def __repr__(self):
        return "<User %r>" % self.username


class BarberRating(db.Model):
    barber_id = db.Column(db.String(100), primary_key=True, nullable=False)
    rating = db.Column(db.Float)
    total_rating = db.Column(db.Integer)


class Style(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    # ids = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    updated_date = db.Column(db.DateTime, default=datetime.utcnow())
    active = db.Column(db.Integer, default=1)

    def to_dict(self):
        """Return information on the style."""
        style_info = {
        "id": self.id,
        "name": self.name,
        "image": self.image,
        "description": self.description,
    }
        return style_info

    def __repr__(self):
        return "<Style %r>" % self.name


"""
db.Integer
primary_key=True
db.String(80)
unique=True
nullable=False
db.Text
db.DateTime
db.Float
db.Boolean
db.PickleType
db.LargeBinary

"""
