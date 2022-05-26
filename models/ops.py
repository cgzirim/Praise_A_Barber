from api.v1 import db
from datetime import datetime


class Review(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    review = db.Column(db.Text)
    user_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)
    barber_id = db.Column(db.String(100), db.ForeignKey("barber.id"), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow())
    updated_date = db.Column(db.DateTime, default=datetime.utcnow())

    def to_dict(self):
        """Returns a dictionary containing informatioin about a review."""
        new_dict = {
            "id": self.id,
            "review": self.review,
            "user_id": self.user_id,
            "barber_id": self.barber_id,
            "created_date": self.created_date,
            "updated_date": self.updated_date,
        }
        return new_dict

    def __repr__(self):
        return "<Review %r>" % self.id
