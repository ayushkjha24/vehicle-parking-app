from controller.database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    pincode = db.Column(db.Integer)
    role = db.Column(db.String(10), default='user')
    reservations = db.relationship('Reservation', backref='user')

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    pincode = db.Column(db.Integer)
    price_per_hour = db.Column(db.Float)
    max_spots = db.Column(db.Integer)
    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete")
    def available_spots(self):
        return sum(1 for spot in self.spots if spot.status == 'A')
    def occupied_spots(self):
        return sum(1 for spot in self.spots if spot.status != 'A')
    def get_available_spot(self):
        for spot in self.spots:
            if spot.status == 'A':
                return spot
        return None

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    status = db.Column(db.String(1), default='A')  # A=Available, O=Occupied
    reservation = db.relationship('Reservation', backref='spot', uselist=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True) # Cost of the reservation
    status = db.Column(db.String(20), default='Booked')

    # calculateing estimated cost based on start time, end time, and spot's lot price
    def estimated_cost(self):
        if not self.start_time or not self.spot or not self.spot.lot:
            return 0
        price_per_hour = self.spot.lot.price_per_hour
        end = self.end_time if self.end_time else datetime.now()
        duration_hours = (end - self.start_time).total_seconds() / 3600
        return round(duration_hours * price_per_hour, 2)
    def location(self):
        if self.spot and self.spot.lot:
            return f"{self.spot.lot.address}, {self.spot.lot.pincode}"
        return "Unknown Location"
    def get_spot_status(self):
        return self.spot.status if self.spot else 'N/A'
    def get_start_time(self):
        if self.start_time:
            return self.start_time.strftime("%Y-%m-%d %H:%M")
        return "N/A"
    def get_end_time(self):
        if self.end_time:
            return self.end_time.strftime("%Y-%m-%d %H:%M")
        return "N/A"
    def get_duration(self):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return duration.total_seconds() // 3600
        elif self.start_time:
            duration = datetime.now() - self.start_time
            return duration.total_seconds() // 3600
        return 0