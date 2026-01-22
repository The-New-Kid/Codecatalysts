from models.model import db, User,ParkingLot,ParkingSpot,Aarti_and_DarshanSlot,PanchangCache,ParkingTimeSlot
import datetime
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
# Create initial users
user1 = User(name="Priyanshu Singh", email="priyanshu@email.com", role=0, password=generate_password_hash("priyanshu123"), pincode="226010", address="Khargapur Gomti nagar Lucknow", mobile_no="1234567890")
user2 = User(name="Shivang Agarwal", email="shivang@email.com", role=1, password=generate_password_hash("shivang123"), pincode="223010", address="Noida-201034", mobile_no="7042213383")
user3=User(name="Tushar Patel",email="tusharpat0701@gmail.com",role=2,password=generate_password_hash("Tushar123"),pincode="201310",address="AB hostel",mobile_no="6389890800")
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
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

slot1 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(6, 0, 0), end_time=datetime.time(9, 0, 0), max_visitors=1)
slot2 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(9, 0, 0), end_time=datetime.time(12, 0, 0), max_visitors=100)
slot3 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(12, 0, 0), end_time=datetime.time(15, 0, 0), max_visitors=100)
slot4 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(15, 0, 0), end_time=datetime.time(18, 0, 0), max_visitors=100)
slot5 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(18, 0, 0), end_time=datetime.time(21, 0, 0), max_visitors=100)

# Create initial aarti slots for a mandir
slot6 = Aarti_and_DarshanSlot(slot_type="Aarti", start_time=datetime.time(5, 0, 0), end_time=datetime.time(6, 0, 0), max_visitors=50)
slot7 = Aarti_and_DarshanSlot(slot_type="Aarti", start_time=datetime.time(12, 0, 0), end_time=datetime.time(13, 0, 0), max_visitors=50)
slot8 = Aarti_and_DarshanSlot(slot_type="Aarti", start_time=datetime.time(18, 0, 0), end_time=datetime.time(19, 0, 0), max_visitors=50)
slot9 = Aarti_and_DarshanSlot(slot_type="Aarti", start_time=datetime.time(20, 0, 0), end_time=datetime.time(21, 0, 0), max_visitors=50)
slot10 = Aarti_and_DarshanSlot(slot_type="Aarti", start_time=datetime.time(21, 0, 0), end_time=datetime.time(22, 0, 0), max_visitors=50)


db.session.add(slot1)
db.session.add(slot2)
db.session.add(slot3)
db.session.add(slot4)
db.session.add(slot5)
db.session.add(slot6)
db.session.add(slot7)
db.session.add(slot8)
db.session.add(slot9)
db.session.add(slot10)
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
p39 = PanchangCache(day=9, month=12, year=2025, tithi="Krishna Panchami")
p40 = PanchangCache(day=10, month=12, year=2025, tithi="Krishna Shashthi")
p41 = PanchangCache(day=11, month=12, year=2025, tithi="Krishna Saptami")
p42 = PanchangCache(day=12, month=12, year=2025, tithi="Krishna Ashtami")
p43 = PanchangCache(day=13, month=12, year=2025, tithi="Krishna Navami")
p44 = PanchangCache(day=14, month=12, year=2025, tithi="Krishna Dashami")
p45 = PanchangCache(day=15, month=12, year=2025, tithi="Krishna Ekadashi")
p46 = PanchangCache(day=16, month=12, year=2025, tithi="Krishna Dwadashi")
p47 = PanchangCache(day=17, month=12, year=2025, tithi="Krishna Trayodashi")
p48 = PanchangCache(day=18, month=12, year=2025, tithi="Krishna Chaturdashi")
p49 = PanchangCache(day=19, month=12, year=2025, tithi="Amavasya")
p50 = PanchangCache(day=20, month=12, year=2025, tithi="Shukla Pratipada")
p51 = PanchangCache(day=21, month=12, year=2025, tithi="Shukla Pratipada")
p52 = PanchangCache(day=22, month=12, year=2025, tithi="Shukla Dwitiya")
p53 = PanchangCache(day=23, month=12, year=2025, tithi="Shukla Tritiya")
p54 = PanchangCache(day=24, month=12, year=2025, tithi="Shukla Chaturthi")
p55 = PanchangCache(day=25, month=12, year=2025, tithi="Shukla Panchami")
p56 = PanchangCache(day=26, month=12, year=2025, tithi="Shukla Shashthi")
p57 = PanchangCache(day=27, month=12, year=2025, tithi="Shukla-Saptami")
p58 = PanchangCache(day=28, month=12, year=2025, tithi="Shukla-Ashtami")
p59 = PanchangCache(day=29, month=12, year=2025, tithi="Shukla-Navami")
p60 = PanchangCache(day=30, month=12, year=2025, tithi="Shukla-Dashami")
p61 = PanchangCache(day=31, month=12, year=2025, tithi="Shukla Dwadashi")

db.session.add_all([
    p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,
    p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,
    p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,
    p31,p32,p33,p34,p35,p36,p37,p38,p39,p40,
    p41,p42,p43,p44,p45,p46,p47,p48,p49,p50,
    p51,p52,p53,p54,p55,p56,p57,p58,p59,p60,
    p61
])
db.session.commit()




start = datetime.datetime.strptime("06:00", "%H:%M")

slots = []
for i in range(10):   # 12 slots * 2 hours = 24 hours
    slot_start = start + timedelta(hours=2*i)
    slot_end = slot_start + timedelta(hours=2)

    # Handle next-day rollover
    if slot_end.day != slot_start.day:
        slot_end = datetime.datetime.combine(slot_start.date(), datetime.datetime.min.time()) + timedelta(days=1)

    slots.append(
        ParkingTimeSlot(
            start_time=slot_start,
            end_time=slot_end
        )
    )

db.session.add_all(slots)
db.session.commit()

print("Dummy 2-hour time slots inserted successfully!")
