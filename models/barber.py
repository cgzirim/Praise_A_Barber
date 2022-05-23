from enum import unique
from api.v1 import db
from datetime import datetime

barber_styles = db.Table('barber_styles',
                         db.Column('barber_id', db.String(100), db.ForeignKey('barber.id'), primary_key=True),
                         db.Column('style_id', db.Integer, db.ForeignKey('style.id'), primary_key=True)
                         )

"""
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


class Barber(db.Model):
    id = db.Column(db.String(100), nullable=False, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Integer)
    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.String(255))
    signup_date = db.Column(db.DateTime, default=datetime.utcnow())  # this should have a default value.
    update_date = db.Column(db.DateTime)
    availability = db.Column(db.Integer, default=0)
    job_count = db.Column(db.Integer, default=0)
    styles = db.relationship('Style', secondary=barber_styles, lazy='subquery',
                             backref=db.backref('barbers', lazy=True))

    def to_dict(self):
        """Returns a dictionary containing a barber's information."""
        new_dict = self.__dict__.copy()

        if 'password' in new_dict:
            new_dict.pop('password')

        if self.styles:
            styles = [style.name for style in self.styles]
            new_dict['styles'] = styles

        new_dict.pop('_sa_instance_state')

        return new_dict

    def __repr__(self):
        return '<User %r>' % self.username


class BarberRating(db.Model):
    barber_id = db.Column(db.String(100), primary_key=True, nullable=False)
    rating = db.Column(db.Float)
    total_rating = db.Column(db.Integer)


class Style(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(100))
    active = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Style %r>' % self.name


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
