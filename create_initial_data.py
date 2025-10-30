from models.model import db, User,ParkingLot,ParkingSpot,DarshanSlot
import datetime
# Create initial users
user1 = User(name="Priyanshu Singh", email="priyanshu@email.com", role=0, password="priyanshu123", pincode="226010", address="Khargapur Gomti nagar Lucknow")
user2 = User(name="Shivang Agarwal", email="shivang@email.com", role=1, password="shivang123", pincode="223010", address="Noida-201034")
db.session.add(user1)
db.session.add(user2)
db.session.commit()


# Create initial parking lots
lot1 = ParkingLot(prime_location_name="Somnath Lot 1", address="Near Somnath Parking Area", pin_code="362530", price_per_hour=40.0, max_spots=30, is_private=False)
lot2 = ParkingLot(prime_location_name="Somnath Lot 2", address="Near Somnath Main Gate", pin_code="362530", price_per_hour=50.0, max_spots=30, is_private=False)
lot3 = ParkingLot(prime_location_name="Somnath Lot 3", address="At Gate No. 4", pin_code="362530", price_per_hour=50.0, max_spots=30, is_private=False)
lot4 = ParkingLot(prime_location_name="Private mandir Lot", address="Near Somnath Mandir", pin_code="362530", price_per_hour=50.0, max_spots=30, is_private=True)
db.session.add(lot1)
db.session.add(lot2)
db.session.add(lot3)
db.session.add(lot4)
db.session.commit()

# Create parking spots for each lot
for lot in [lot1, lot2, lot3, lot4]:
    for _ in range(lot.max_spots):
        spot = ParkingSpot(lot_id=lot.id, status='A')
        db.session.add(spot)
db.session.commit()

# Create initial darshan slots for a mandir

slot1 = DarshanSlot(mandir_id=1, slot_type="Darshan", start_time=datetime.time(6, 0, 0), end_time=datetime.time(9, 0, 0), max_visitors=200)
slot2 = DarshanSlot(mandir_id=1, slot_type="Darshan", start_time=datetime.time(9, 0, 0), end_time=datetime.time(12, 0, 0), max_visitors=100)
slot3 = DarshanSlot(mandir_id=1, slot_type="Darshan", start_time=datetime.time(12, 0, 0), end_time=datetime.time(15, 0, 0), max_visitors=100)
slot4 = DarshanSlot(mandir_id=1, slot_type="Darshan", start_time=datetime.time(15, 0, 0), end_time=datetime.time(18, 0, 0), max_visitors=100)
slot5 = DarshanSlot(mandir_id=1, slot_type="Darshan", start_time=datetime.time(18, 0, 0), end_time=datetime.time(21, 0, 0), max_visitors=100)

db.session.add(slot1)
db.session.add(slot2)
db.session.add(slot3)
db.session.add(slot4)
db.session.add(slot5)
db.session.commit()

