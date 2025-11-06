from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role=db.Column(db.Integer,default=1)
    password = db.Column(db.String(200), nullable=False)
    reservations = db.relationship('Reservation', backref='user', cascade="all, delete")
    pincode = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)

class ParkingLot(db.Model):
    __tablename__ = 'parking_lots'
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    max_spots = db.Column(db.Integer, nullable=False)
    spots = db.relationship('ParkingSpot', backref='lot', cascade="all, delete")
    revenue = db.Column(db.Float, default=0.0)
    is_private = db.Column(db.Boolean, default=False) 
    
class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id',ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(1), default='A')  # 'A' = Available, 'O' = Occupied
    reservation = db.relationship('Reservation', backref='spot', uselist=False, cascade="all, delete")
     
class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id',ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=True)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    cost_per_hour = db.Column(db.Float, nullable=False)

class Mandir(db.Model):
    __tablename__ = 'mandirs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    slots = db.relationship('DarshanSlot', backref='mandir', cascade="all, delete")

class DarshanSlot(db.Model):
    __tablename__ = 'darshan_slots'
    id = db.Column(db.Integer, primary_key=True)
    mandir_id = db.Column(db.Integer, db.ForeignKey('mandirs.id', ondelete='CASCADE'), nullable=False)
    slot_type = db.Column(db.String(20), nullable=False)  # e.g., 'Darshan' or 'Arti'
    start_time = db.Column(db.Time, nullable=False)       # ✅ only Time now
    end_time = db.Column(db.Time, nullable=False)
    max_visitors = db.Column(db.Integer, nullable=False)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('darshan_slots.id', ondelete='CASCADE'), nullable=False)
    qr_code = db.Column(db.String(200), nullable=True)  
    status = db.Column(db.String(20), default='Booked')  
    scan_count = db.Column(db.Integer, default=0)  # NEW FIELD to track scans
    user = db.relationship('User', backref='tickets')
    slot = db.relationship('DarshanSlot', backref='tickets')


class TicketParking(db.Model):
    __tablename__ = 'ticket_parking'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id', ondelete='CASCADE'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id', ondelete='CASCADE'), nullable=False)
    qr_code = db.Column(db.String(200), nullable=True)
