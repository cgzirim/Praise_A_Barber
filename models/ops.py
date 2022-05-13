from app.v1.app import db


class Comments(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    comment = db.Column(db.Text)
    user_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)
    barber_id = db.Column(db.String(100), db.ForeignKey('barber.id'), nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.id

