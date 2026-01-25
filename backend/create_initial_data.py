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
lot1 = ParkingLot(prime_location_name="Bake Bihari Lot 1", address="Near Bake Bihari Parking Area", pin_code="362530", price_per_hour=40.0, max_spots=30, is_private=False)
lot2 = ParkingLot(prime_location_name="Bake Bihari Lot 2", address="Near Bake Bihari Main Gate", pin_code="362530", price_per_hour=50.0, max_spots=30, is_private=False)
lot3 = ParkingLot(prime_location_name="Bake Bihari Lot 3", address="At Gate No. 4", pin_code="362530", price_per_hour=50.0, max_spots=30, is_private=False)
lot4 = ParkingLot(prime_location_name="Private mandir Lot", address="Near Bake Bihari Mandir", pin_code="362530", price_per_hour=50.0, max_spots=30, is_private=True)
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

slot1 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(6, 0, 0), end_time=datetime.time(9, 0, 0), max_visitors=2)
slot2 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(9, 0, 0), end_time=datetime.time(12, 0, 0), max_visitors=2)
slot3 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(12, 0, 0), end_time=datetime.time(15, 0, 0), max_visitors=2)
slot4 = Aarti_and_DarshanSlot(slot_type="Darshan", start_time=datetime.time(15, 0, 0), end_time=datetime.time(18, 0, 0), max_visitors=2)

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
db.session.add(slot6)
db.session.add(slot7)
db.session.add(slot8)
db.session.add(slot9)
db.session.add(slot10)
db.session.commit()


p31 = PanchangCache(day=1, month=12, year=2025, tithi="Shukla-Ekadashi", fest=None, crowd=24894)
p32 = PanchangCache(day=2, month=12, year=2025, tithi="Shukla Dwadashi", fest=None, crowd=24887)
p33 = PanchangCache(day=3, month=12, year=2025, tithi="Shukla Trayodashi", fest=None, crowd=24912)
p34 = PanchangCache(day=4, month=12, year=2025, tithi="Shukla Chaturdashi", fest=None, crowd=24931)
p35 = PanchangCache(day=5, month=12, year=2025, tithi="Krishna Pratipada", fest=None, crowd=25324)
p36 = PanchangCache(day=6, month=12, year=2025, tithi="Krishna Dwitiya", fest=None, crowd=26396)
p37 = PanchangCache(day=7, month=12, year=2025, tithi="Krishna Tritiya", fest=None, crowd=26964)
p38 = PanchangCache(day=8, month=12, year=2025, tithi="Krishna Chaturthi", fest=None, crowd=24999)
p39 = PanchangCache(day=9, month=12, year=2025, tithi="Krishna Panchami", fest=None, crowd=24976)
p40 = PanchangCache(day=10, month=12, year=2025, tithi="Krishna Shashthi", fest=None, crowd=24979)
p41 = PanchangCache(day=11, month=12, year=2025, tithi="Krishna Saptami", fest=None, crowd=24969)
p42 = PanchangCache(day=12, month=12, year=2025, tithi="Krishna Ashtami", fest=None, crowd=25327)
p43 = PanchangCache(day=13, month=12, year=2025, tithi="Krishna Navami", fest=None, crowd=26358)
p44 = PanchangCache(day=14, month=12, year=2025, tithi="Krishna Dashami", fest=None, crowd=26880)
p45 = PanchangCache(day=15, month=12, year=2025, tithi="Krishna Ekadashi", fest=None, crowd=24865)
p46 = PanchangCache(day=16, month=12, year=2025, tithi="Krishna Dwadashi", fest=None, crowd=24789)
p47 = PanchangCache(day=17, month=12, year=2025, tithi="Krishna Trayodashi", fest=None, crowd=24738)
p48 = PanchangCache(day=18, month=12, year=2025, tithi="Krishna Chaturdashi", fest=None, crowd=24673)
p49 = PanchangCache(day=19, month=12, year=2025, tithi="Amavasya", fest=None, crowd=24977)
p50 = PanchangCache(day=20, month=12, year=2025, tithi="Shukla Pratipada", fest=None, crowd=25955)
p51 = PanchangCache(day=21, month=12, year=2025, tithi="Shukla Pratipada", fest=None, crowd=26429)
p52 = PanchangCache(day=22, month=12, year=2025, tithi="Shukla Dwitiya", fest=None, crowd=24369)
p53 = PanchangCache(day=23, month=12, year=2025, tithi="Shukla Tritiya", fest=None, crowd=24254)
p54 = PanchangCache(day=24, month=12, year=2025, tithi="Shukla Chaturthi", fest=None, crowd=24170)
p55 = PanchangCache(day=25, month=12, year=2025, tithi="Shukla Panchami", fest=None, crowd=25135)
p56 = PanchangCache(day=26, month=12, year=2025, tithi="Shukla Shashthi", fest=None, crowd=25422)
p57 = PanchangCache(day=27, month=12, year=2025, tithi="Shukla-Saptami", fest=None, crowd=25336)
p58 = PanchangCache(day=28, month=12, year=2025, tithi="Shukla-Ashtami", fest=None, crowd=25810)
p59 = PanchangCache(day=29, month=12, year=2025, tithi="Shukla-Navami", fest=None, crowd=24814)
p60 = PanchangCache(day=30, month=12, year=2025, tithi="Shukla-Dashami", fest=None, crowd=24717)
p61 = PanchangCache(day=31, month=12, year=2025, tithi="Shukla Dwadashi", fest=None, crowd=24659)
p62 = PanchangCache(day=1, month=1, year=2026, tithi="Shukla Trayodashi", fest=None, crowd=24451)
p63 = PanchangCache(day=2, month=1, year=2026, tithi="Shukla Chaturdashi", fest=None, crowd=23800)
p64 = PanchangCache(day=3, month=1, year=2026, tithi="Purnima", fest=None, crowd=24741)
p65 = PanchangCache(day=4, month=1, year=2026, tithi="Krishna Pratipada", fest=None, crowd=25267)
p66 = PanchangCache(day=5, month=1, year=2026, tithi="Krishna Dwitiya", fest=None, crowd=23349)
p67 = PanchangCache(day=6, month=1, year=2026, tithi="Krishna Tritiya", fest=None, crowd=23312)
p68 = PanchangCache(day=7, month=1, year=2026, tithi="Krishna Panchami", fest=None, crowd=23315)
p69 = PanchangCache(day=8, month=1, year=2026, tithi="Krishna Shashthi", fest=None, crowd=23319)
p70 = PanchangCache(day=9, month=1, year=2026, tithi="Krishna Saptami", fest=None, crowd=23706)
p71 = PanchangCache(day=10, month=1, year=2026, tithi="Krishna Saptami", fest=None, crowd=24703)
p72 = PanchangCache(day=11, month=1, year=2026, tithi="Krishna Ashtami", fest=None, crowd=25281)
p73 = PanchangCache(day=12, month=1, year=2026, tithi="Krishna Navami", fest=None, crowd=23410)
p74 = PanchangCache(day=13, month=1, year=2026, tithi="Krishna Dashami", fest=None, crowd=23413)
p75 = PanchangCache(day=14, month=1, year=2026, tithi="Krishna Ekadashi", fest="Makar Sankranti", crowd=26095)
p76 = PanchangCache(day=15, month=1, year=2026, tithi="Krishna Dwadashi", fest=None, crowd=23480)
p77 = PanchangCache(day=16, month=1, year=2026, tithi="Krishna Trayodashi", fest=None, crowd=23884)
p78 = PanchangCache(day=17, month=1, year=2026, tithi="Krishna Chaturdashi", fest=None, crowd=24890)
p79 = PanchangCache(day=18, month=1, year=2026, tithi="Amavasya", fest=None, crowd=25469)
p80 = PanchangCache(day=19, month=1, year=2026, tithi="Shukla Pratipada", fest=None, crowd=23590)
p81 = PanchangCache(day=20, month=1, year=2026, tithi="Shukla Dwitiya", fest=None, crowd=23577)
p82 = PanchangCache(day=21, month=1, year=2026, tithi="Shukla Tritiya", fest=None, crowd=23590)
p83 = PanchangCache(day=22, month=1, year=2026, tithi="Shukla Chaturthi", fest=None, crowd=23590)
p84 = PanchangCache(day=23, month=1, year=2026, tithi="Shukla Panchami", fest="Saraswati Puja", crowd=26605)
p85 = PanchangCache(day=24, month=1, year=2026, tithi="Shukla Shashthi", fest=None, crowd=24925)
p86 = PanchangCache(day=25, month=1, year=2026, tithi="Shukla-Saptami", fest=None, crowd=25461)
p87 = PanchangCache(day=26, month=1, year=2026, tithi="Shukla-Ashtami", fest=None, crowd=24516)
p88 = PanchangCache(day=27, month=1, year=2026, tithi="Shukla-Navami", fest=None, crowd=23479)
p89 = PanchangCache(day=28, month=1, year=2026, tithi="Shukla-Dashami", fest=None, crowd=23447)
p90 = PanchangCache(day=29, month=1, year=2026, tithi="Shukla-Ekadashi", fest=None, crowd=23404)
p91 = PanchangCache(day=30, month=1, year=2026, tithi="Shukla Dwadashi", fest=None, crowd=23734)
p92 = PanchangCache(day=31, month=1, year=2026, tithi="Shukla Trayodashi", fest=None, crowd=24666)
db.session.add_all([
    p31, p32, p33, p34, p35, p36, p37, p38, p39, p40,
    p41, p42, p43, p44, p45, p46, p47, p48, p49, p50,
    p51, p52, p53, p54, p55, p56, p57, p58, p59, p60,
    p61, p62, p63, p64, p65, p66, p67, p68, p69, p70,
    p71, p72, p73, p74, p75, p76, p77, p78, p79, p80,
    p81, p82, p83, p84, p85, p86, p87, p88, p89, p90,
    p91, p92
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
