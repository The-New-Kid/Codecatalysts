from models.model import db, User,ParkingLot,ParkingSpot,DarshanSlot,PanchangCache
import datetime
# Create initial users
user1 = User(name="Priyanshu Singh", email="priyanshu@email.com", role=0, password="priyanshu123", pincode="226010", address="Khargapur Gomti nagar Lucknow", mobile_no="1234567890")
user2 = User(name="Shivang Agarwal", email="shivang@email.com", role=1, password="shivang123", pincode="223010", address="Noida-201034", mobile_no="7042213383")
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

slot1 = DarshanSlot(slot_type="Darshan", start_time=datetime.time(6, 0, 0), end_time=datetime.time(9, 0, 0), max_visitors=1)
slot2 = DarshanSlot(slot_type="Darshan", start_time=datetime.time(9, 0, 0), end_time=datetime.time(12, 0, 0), max_visitors=100)
slot3 = DarshanSlot(slot_type="Darshan", start_time=datetime.time(12, 0, 0), end_time=datetime.time(15, 0, 0), max_visitors=100)
slot4 = DarshanSlot(slot_type="Darshan", start_time=datetime.time(15, 0, 0), end_time=datetime.time(18, 0, 0), max_visitors=100)
slot5 = DarshanSlot(slot_type="Darshan", start_time=datetime.time(18, 0, 0), end_time=datetime.time(21, 0, 0), max_visitors=100)

db.session.add(slot1)
db.session.add(slot2)
db.session.add(slot3)
db.session.add(slot4)
db.session.add(slot5)
db.session.commit()



p1 = PanchangCache(day=1, month=11, year=2025, tithi="Shukla-Dashami")
p2 = PanchangCache(day=2, month=11, year=2025, tithi="Shukla Dwadashi")
p3 = PanchangCache(day=3, month=11, year=2025, tithi="Shukla Trayodashi")
p4 = PanchangCache(day=4, month=11, year=2025, tithi="Shukla Chaturdashi")
p5 = PanchangCache(day=5, month=11, year=2025, tithi="Purnima")
p6 = PanchangCache(day=6, month=11, year=2025, tithi="Krishna Pratipada")
p7 = PanchangCache(day=7, month=11, year=2025, tithi="Krishna Dwitiya")
p8 = PanchangCache(day=8, month=11, year=2025, tithi="Krishna Chaturthi")
p9 = PanchangCache(day=9, month=11, year=2025, tithi="Krishna Panchami")
p10 = PanchangCache(day=10, month=11, year=2025, tithi="Krishna Shashthi")
p11 = PanchangCache(day=11, month=11, year=2025, tithi="Krishna Saptami")
p12 = PanchangCache(day=12, month=11, year=2025, tithi="Krishna Ashtami")
p13 = PanchangCache(day=13, month=11, year=2025, tithi="Krishna Navami")
p14 = PanchangCache(day=14, month=11, year=2025, tithi="Krishna Dashami")
p15 = PanchangCache(day=15, month=11, year=2025, tithi="Krishna Ekadashi")
p16 = PanchangCache(day=16, month=11, year=2025, tithi="Krishna Dwadashi")
p17 = PanchangCache(day=17, month=11, year=2025, tithi="Krishna Trayodashi")
p18 = PanchangCache(day=18, month=11, year=2025, tithi="Krishna Chaturdashi")
p19 = PanchangCache(day=19, month=11, year=2025, tithi="Krishna Chaturdashi")
p20 = PanchangCache(day=20, month=11, year=2025, tithi="Amavasya")
p21 = PanchangCache(day=21, month=11, year=2025, tithi="Shukla Pratipada")
p22 = PanchangCache(day=22, month=11, year=2025, tithi="Shukla Dwitiya")
p23 = PanchangCache(day=23, month=11, year=2025, tithi="Shukla Tritiya")
p24 = PanchangCache(day=24, month=11, year=2025, tithi="Shukla Chaturthi")
p25 = PanchangCache(day=25, month=11, year=2025, tithi="Shukla Panchami")
p26 = PanchangCache(day=26, month=11, year=2025, tithi="Shukla Shashthi")
p27 = PanchangCache(day=27, month=11, year=2025, tithi="Shukla-Saptami")
p28 = PanchangCache(day=28, month=11, year=2025, tithi="Shukla-Ashtami")
p29 = PanchangCache(day=29, month=11, year=2025, tithi="Shukla-Navami")
p30 = PanchangCache(day=30, month=11, year=2025, tithi="Shukla-Dashami")
p31 = PanchangCache(day=1, month=12, year=2025, tithi="Shukla-Ekadashi")
p32 = PanchangCache(day=2, month=12, year=2025, tithi="Shukla Dwadashi")
p33 = PanchangCache(day=3, month=12, year=2025, tithi="Shukla Trayodashi")
p34 = PanchangCache(day=4, month=12, year=2025, tithi="Shukla Chaturdashi")
p35 = PanchangCache(day=5, month=12, year=2025, tithi="Krishna Pratipada")
p36 = PanchangCache(day=6, month=12, year=2025, tithi="Krishna Dwitiya")
p37 = PanchangCache(day=7, month=12, year=2025, tithi="Krishna Tritiya")
p38 = PanchangCache(day=8, month=12, year=2025, tithi="Krishna Chaturthi")


db.session.add_all([
    p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,
    p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,
    p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,
    p31,p32,p33,p34,p35,p36,p37,p38
])
db.session.commit()
