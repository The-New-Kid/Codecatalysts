from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_no = db.Column(db.String(15), unique=True, nullable=False)
    role=db.Column(db.Integer,default=1)
    password = db.Column(db.String(200), nullable=False)
    public_reservation = db.relationship('PublicReservation', backref='user', cascade="all, delete")
    private_reservation = db.relationship('PrivateReservation', backref='user', cascade="all, delete")
    
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
    time_slot_id=db.Column(db.Integer,db.ForeignKey('parking_time_slots.id'))

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id',ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(1), default='A')  # 'A' = Available, 'O' = Occupied
    #reservation = db.relationship('Reservation', backref='spot', uselist=False, cascade="all, delete")

class ParkingTimeSlot(db.Model):
    __tablename__ = 'parking_time_slots'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)


class PublicReservation(db.Model):
    __tablename__ = 'public_reservations'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id',ondelete='CASCADE'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id',ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=True)
    date_of_parking = db.Column(db.Date, nullable=False)
    timeslot_id = db.Column(db.Integer, db.ForeignKey('parking_time_slots.id',ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('spot_id', 'date_of_parking', 'timeslot_id', name='unique_public_reservation'),)

class PrivateReservation(db.Model):
    __tablename__ = 'private_reservations'
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id',ondelete='CASCADE'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id',ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=True)
    date_of_parking = db.Column(db.Date, nullable=False)
    timeslot_id = db.Column(db.Integer, db.ForeignKey('parking_time_slots.id',ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('spot_id', 'date_of_parking', 'timeslot_id', name='unique_private_reservation'),)


# class Reservation(db.Model):
#     __tablename__ = 'reservations'
#     id = db.Column(db.Integer, primary_key=True)
#     spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id',ondelete='CASCADE'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
#     vehicle_number = db.Column(db.String(20), nullable=True)
#     parking_timestamp = db.Column(db.DateTime, nullable=False)
#     leaving_timestamp = db.Column(db.DateTime, nullable=True)
#     cost_per_hour = db.Column(db.Float, nullable=False)

# class TicketParking(db.Model):
#     __tablename__ = 'ticket_parking'
#     id = db.Column(db.Integer, primary_key=True)
#     spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id', ondelete='CASCADE'), nullable=False)
#     qr_code = db.Column(db.String(200), nullable=True)

class Aarti_and_DarshanSlot(db.Model):
    __tablename__ = 'darshan_slots'
    id = db.Column(db.Integer, primary_key=True)
    slot_type = db.Column(db.String(20), nullable=False)  # e.g., 'Darshan' or 'Arti'
    start_time = db.Column(db.Time, nullable=False)       # ✅ only Time now
    end_time = db.Column(db.Time, nullable=False)
    max_visitors = db.Column(db.Integer, nullable=False)

#relationship bw passenger aarti,need to be reworked

class Passenger(db.Model):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    aadhaar_number = db.Column(db.String(12), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    qr_code = db.Column(db.String(200))
    scan_count = db.Column(db.Integer, default=0)
    slot = db.relationship('Aarti_and_DarshanSlot', backref='passengers')
    darshan_date = db.Column(db.Date, nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('darshan_slots.id', ondelete='CASCADE'), nullable=False)
    special=db.Column(db.Boolean, default=False)
    with_special=db.Column(db.Boolean, default=False)
    age=db.Column(db.Integer,nullable=False)
    gender=db.Column(db.String(10),nullable=False)
    priority=db.Column(db.Integer,default=0)
    wheelchairneeded=db.Column(db.Boolean,default=False)


class SevaBooking(db.Model):
    __tablename__ = 'seva_bookings'
    id = db.Column(db.Integer, primary_key=True)
    seva_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    qr_code = db.Column(db.String(200))
    user = db.relationship('User', backref='seva_bookings')

class PanchangCache(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    tithi = db.Column(db.String(100), nullable=False)
    fest=db.Column(db.String(100),nullable=True)
    crowd=db.Column(db.Integer,nullable=True)
    __table_args__ = (
        db.UniqueConstraint('day', 'month', 'year', name='unique_date_tithi'),
    )


