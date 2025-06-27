from controller.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    pincode = db.Column(db.String(6))
    role = db.Column(db.String(10), default='user')
    reservations = db.relationship('Reservation', backref='user')

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    pincode = db.Column(db.String(6))
    price_per_hour = db.Column(db.Float)
    max_spots = db.Column(db.Integer)
    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete")

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    status = db.Column(db.String(1), default='A')  # A=Available, O=Occupied
    reservation = db.relationship('Reservation', backref='spot', uselist=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True)
