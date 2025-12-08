import ast
from flask import request,current_app as app,make_response,send_from_directory
from flask_restful import Api,Resource,fields, marshal_with,marshal
from models.model import *
import mimetypes
import os
import requests
import calendar
#from pyzbar.pyzbar import decode
from PIL import Image
import base64 as Base64
import time
import random
from datetime import datetime
from werkzeug.utils import secure_filename
import qrcode
from twilio.rest import Client
from dotenv import load_dotenv
from flask import request
from flask_restful import Resource
from sqlalchemy import and_
from datetime import timedelta
import json
import cv2
from gittest import super
load_dotenv()
api=Api(prefix='/api')
otp_login_storage = {}
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
CONTENT_SID = os.getenv("CONTENT_SID")
clouflare_url="asd"
TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

AADHAR_MOBILE_MAP = {
    "111122223333": "+917042213383",
    "222233334444": "+916396081309",
    "333344445555": "+919900112233",
    "444455556666": "+919988776655",
    "555566667777": "+919911223344",
    "666677778888": "+919922334455",
}

otp_storage = {}
def qrgenerator(data,filename):
            QR_FOLDER = os.path.join("static", "qrcode")
            os.makedirs(QR_FOLDER, exist_ok=True)

            qr_data_bytes=data.encode('utf-8')
            qr_data=Base64.b64encode(qr_data_bytes)
            qr_img = qrcode.make(qr_data)
            qr_path = os.path.join(QR_FOLDER, filename)
            qr_img.convert('RGB').save(qr_path, 'PNG')
            return qr_data

class SendOtpResource(Resource):
    def post(self):
        data = request.get_json()
        aadhar = data.get("aadhar")

        if not aadhar:
            return {"success": False, "message": "Aadhar missing"}, 400

        mobile = AADHAR_MOBILE_MAP.get(aadhar)
        if not mobile:
            return {"success": False, "message": "Aadhar not registered"}, 404

        otp = str(random.randint(100000, 999999))
        otp_storage[aadhar] = otp

        try:
            TWILIO_CLIENT.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=f"Your OTP for DevDhamPath Booking is {otp}",
                to=f"whatsapp:{mobile}"
            )
            return {"success": True, "message": f"OTP sent to {mobile}"}, 200

        except Exception as e:
            return {"success": False, "message": str(e)}, 500

class VerifyOtpResource(Resource):
    def post(self):
        data = request.get_json()
        aadhar = data.get("aadhar")
        otp = data.get("otp")

        stored = otp_storage.get(aadhar)
        if stored and stored == otp:
            return {"success": True, "message": "OTP Verified"}, 200

        return {"success": False, "message": "Invalid OTP"}, 400

class ImageserverResource(Resource):
    def get(self, filename):
        base_path = os.path.abspath(os.path.join(app.root_path, '..', 'static', 'qrcode'))
        response = make_response(send_from_directory(base_path, filename))
        response.headers['Content-Type'] = mimetypes.guess_type(filename)[0] or 'image/png'
        return response

class MobileLoginResource(Resource):
    def post(self):
        data = request.get_json()
        mobile_number = data.get('mobile_number')

        if not mobile_number:
            return {"message": "Mobile number required"}, 400

        if not mobile_number.isdigit() or len(mobile_number) != 10:
            return {"message": "Invalid mobile number"}, 400

        user = User.query.filter_by(mobile_no=mobile_number).first()
        if not user:
            return {"message": "User not found"}, 404

        otp = str(random.randint(100000, 999999))

        otp_login_storage[mobile_number] = {
            "otp": otp,
            "created": time.time()
        }

        try:
            TWILIO_CLIENT.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=f"Your OTP for DevDhamPath Login is {otp}",
                to=f"whatsapp:+91{mobile_number}"
            )
        except Exception:
            return {"message": "OTP service failed"}, 500
        
        return {"message": "OTP sent successfully"}, 200

class LoginverifyotpResource(Resource):
    def post(self):
        data = request.get_json()
        otp = data.get('otp')
        mobile_number = data.get('mobile_number')
        if not otp or not mobile_number:
            return {"message": "Mobile number and OTP required"}, 400
        stored = otp_login_storage.get(mobile_number)
        if not stored:
            return {"message": "OTP not generated"}, 400

        if time.time() - stored['created'] > 120:
            otp_login_storage.pop(mobile_number, None)
            return {"message": "OTP expired"}, 400

        if otp != stored['otp']:
            return {"message": "Wrong OTP"}, 401

        user = User.query.filter_by(mobile_no=mobile_number).first()
        if not user:
            return {"message": "User not found"}, 404

        role = "admin" if user.role == 0 else "user"

        otp_login_storage.pop(mobile_number, None)

        return {
            "message": "Login successful",
            "user_id": user.id,
            "role": role,
            "name": user.name
        }, 200
api.add_resource(MobileLoginResource, '/mobile-login')
api.add_resource(LoginverifyotpResource, '/login-verify-otp')
api.add_resource(ImageserverResource,'/qrcode/<string:filename>')
api.add_resource(VerifyOtpResource, '/verify-otp')
api.add_resource(SendOtpResource, '/send-otp')

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"message": "Email and password required"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User not found"}, 404

        if user.password != password:
            return {"message": "Incorrect password"}, 401

        # Map 0/1 → "admin"/"user"
        role = "admin" if user.role == 0 else "user"

        return {
            "message": "Login successful",
            "user_id": user.id,
            "role": role,
            "name": user.name
        }, 200
api.add_resource(LoginResource, '/login')

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        pincode = data.get('pincode')
        address = data.get('address')
        mobile_no=data.get('mobile_no')
        email=email.lower()
        if not all([name, email, password, pincode, address]):
            return {"message": "All fields are required"}, 400

        # Check duplicate
        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered"}, 409
        if User.query.filter_by(mobile_no=mobile_no).first():
            return {"message": "Mobile number already registered"}, 409
        # Create user
        new_user = User(name=name, email=email, password=password,
                        pincode=pincode, address=address,mobile_no=mobile_no)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Registration successful"}, 201


api.add_resource(RegisterResource, '/register')


class UserDashboardResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        reservations = []
        for r in user.public_reservation:  # assuming relationship exists
            reservations.append({
                "id": r.id,
                "prime_location": r.spot.lot.prime_location_name,
                "address": r.spot.lot.address,
                "vehicle_number": r.vehicle_number,
                "start_time": r.parking_timestamp.strftime("%d-%m-%Y %I:%M %p"),
                "end_time": r.leaving_timestamp.strftime("%d-%m-%Y %I:%M %p") if r.leaving_timestamp else None,
                "cost_per_hour": r.cost_per_hour,
            })

        return {
            "user": {
                "id": user.id,
                "name": user.name,
            },
            "reservations": reservations
        }, 200


api.add_resource(UserDashboardResource, '/user/dashboard/<int:user_id>')

##WORK LEFT
class UserProfileResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "pincode": user.pincode,
            "address": user.address,
            "mobile_no": user.mobile_no
        }, 200

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.pincode = data.get('pincode', user.pincode)
        user.address = data.get('address', user.address)
        user.mobile_no = data.get('mobile_no', user.mobile_no)
        # Add validation to ensure unique email/mobile
        existing_email_user = User.query.filter_by(email=user.email).first()
        if existing_email_user and existing_email_user.id != user.id:
            return {"message": "Email already in use"}, 409
    
        existing_mobile_user = User.query.filter_by(mobile_no=user.mobile_no).first()
        if existing_mobile_user and existing_mobile_user.id != user.id:
            return {"message": "Mobile number already in use"}, 409   
    
        db.session.commit()
        return {"message": "Profile updated successfully"}, 200

api.add_resource(UserProfileResource, '/user/<int:user_id>')

class BookTicketDataResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        type=request.args.get('type')
        
        if not user:
            return {"message": "User not found"}, 404



        slots = Aarti_and_DarshanSlot.query.filter_by(slot_type=type).order_by(Aarti_and_DarshanSlot.start_time).all()
        lots = ParkingLot.query.all()

        return {
            "user": {"id": user.id, "name": user.name},
            "slots": [
                {
                    "id": s.id,
                    "slot_type": s.slot_type,
                    "start": s.start_time.strftime("%H:%M"),
                    "end": s.end_time.strftime("%H:%M"),
                    "max_visitors": s.max_visitors
                } for s in slots
            ],
            "parking_lots": [
                {"id": p.id, "name": p.prime_location_name} for p in lots
            ]
        }, 200


api.add_resource(BookTicketDataResource, '/book-ticket/<int:user_id>')


# -------------------------------------------
#  BOOK TICKET (UPDATED LOGIC)
# -------------------------------------------
class BookTicketResource(Resource):
    def post(self):
        data = request.get_json()
        print("Booking Data:", data)

        user_id = data.get("user_id")
        slot_id = data.get("slot_id")
        darshan_date = data.get("darshan_date")
        passengers = data.get("passengers")
        mobile_number = data.get("mobile_number")

        if not darshan_date:
            return {"success": False, "message": "Darshan date missing"}, 400

        user = User.query.get(user_id)
        slot = Aarti_and_DarshanSlot.query.get(slot_id)

        if not user or not slot:
            return {"success": False, "message": "Invalid user or slot"}, 400

        try:
            selected_date = datetime.strptime(darshan_date, "%Y-%m-%d").date()
        except:
            return {"success": False, "message": "Invalid date format"}, 400

        num_members = len(passengers)

        already_booked = db.session.query(Passenger)\
            .filter(
                Passenger.slot_id == slot_id,
                Passenger.darshan_date == selected_date
            ).count()

        if already_booked + num_members > slot.max_visitors:
            return {
                "success": False,
                "message": f"Only {slot.max_visitors - already_booked} slots left"
            }, 400
        

        QR_FOLDER = os.path.join("static", "qrcode")
        os.makedirs(QR_FOLDER, exist_ok=True)

        booked_passengers = []

        for p in passengers:
            name = p.get("name")
            aadhar = p.get("aadhar")
            otp_entered = p.get("otp")
            is_special=p.get("speciallyAbled",False)
            with_special=p.get("accompanying",False)
            if otp_storage.get(aadhar) != otp_entered:
                return {"success": False, "message": f"OTP failed for {name}"}, 400

            otp_storage.pop(aadhar, None)

            passenger = Passenger(
                user_id=user.id,
                slot_id=slot.id,
                darshan_date=selected_date,
                name=name,
                special=is_special,
                with_special=with_special,
                aadhaar_number=aadhar
            )
            db.session.add(passenger)
            db.session.flush()

            qr_data = str({"name":name,"passenger_id":passenger.id, "darshan_date":darshan_date, "slot_id":slot_id,"adhaar":aadhar,"special":is_special,"with_special":with_special})
            qr_filename = f"passenger_{passenger.id}_{secure_filename(name)}.png"
            encoded=qrgenerator(qr_data,qr_filename)
            passenger.qr_code = encoded
            print(qr_filename)
            try:
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=f"Ticket #{passenger.id} booked for {name} at {slot.start_time.strftime('%Y-%m-%d %H:%M')}",
                    to=f"whatsapp:+91{mobile_number}"
                )
                
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=f"Ticket #{passenger.id} booked for {name} at {slot.start_time.strftime('%Y-%m-%d %H:%M')}",
                    media_url=[f"{clouflare_url}/api/qrcode/{qr_filename}"],         ##Cloudflareee
                    to=f"whatsapp:+91{mobile_number}"
                )
            except Exception as e:
                print("WhatsApp Error:", e)

            booked_passengers.append({
                "passenger_id": passenger.id,
                "qr_code": qr_filename
            })

        db.session.commit()

        return {
            "success": True,
            "passengers": booked_passengers
        }, 200

api.add_resource(BookTicketResource, '/book-ticket')
# -------------------------------------------
API_USER = os.getenv("CALANDER_UID")
API_KEY = os.getenv("CALANDER_API_KEY")

# class PanchangMonthResource(Resource):
#     def post(self):
#         data = request.get_json()
#         month = data["month"]
#         year = data["year"]
#         list_hindu=super(year=year,month=month)
#         total_days = calendar.monthrange(year, month)[1]

#         result = {}

#         for day in range(1, total_days + 1):

#             # 1. Check cache
#             cached = PanchangCache.query.filter_by(
#                 day=day, month=month, year=year
#             ).first()

#             if cached:
#                 result[day] = cached.tithi
#                 continue

#             # 2. Call Astrology API if not cached
#             payload = {
#                 "day": day,
#                 "month": month,
#                 "year": year,
#                 "hour": 7,
#                 "min": 45,
#                 "lat": 19.132,
#                 "lon": 72.342,
#                 "tzone": 5.5
#             }

#             response = requests.post(
#                 "https://json.astrologyapi.com/v1/basic_panchang",
#                 json=payload,
#                 auth=(API_USER, API_KEY)
#             )

#             tithi = response.json().get("tithi")

#             # 3. Save in DB
#             new_entry = PanchangCache(
#                 day=day,
#                 month=month,
#                 year=year,
#                 tithi=tithi
#             )
#             db.session.add(new_entry)
#             db.session.commit()

#             result[day] = tithi

#         return result, 200
class PanchangMonthResource(Resource):
    def post(self):
        data = request.get_json()
        month = data["month"]
        year = data["year"]
        print(type(month),type(year))
        list_hindu = super(year=str(year), month=month) or []    
        print(list_hindu)
        # Convert festival list into dictionary: {day: fest_name}
        festival_map = {}
        for item in list_hindu:
            try:
                d = int(item.get("date"))
                n = item.get("name")
                if d and n:
                    festival_map[d] = n
            except:
                pass

        total_days = calendar.monthrange(year, month)[1]
        print("fest:",festival_map)
        result = {}

        for day in range(1, total_days + 1):
            fest = festival_map.get(day)
            cached = PanchangCache.query.filter_by(
                day=day, month=month, year=year
            ).first()

            if cached:
                result[day] = {
                    "tithi": cached.tithi,
                    "fest":fest
                }
                continue

            payload = {
                "day": day,
                "month": month,
                "year": year,
                "hour": 7,
                "min": 45,
                "lat": 19.132,
                "lon": 72.342,
                "tzone": 5.5
            }

            response = requests.post(
                "https://json.astrologyapi.com/v1/basic_panchang",
                json=payload,
                auth=(API_USER, API_KEY)
            )
            
            tithi = response.json().get("tithi")
              # check if this day has a festival

            new_entry = PanchangCache(
                day=day,
                month=month,
                year=year,
                tithi=tithi,
                fest=fest
            )
            db.session.add(new_entry)
            db.session.commit()

            result[day] = {
                "tithi": tithi,
                "fest": fest
            }
        return result, 200


api.add_resource(PanchangMonthResource, "/calender/month")


# ============================
# ADMIN: PARKING LOTS OVERVIEW
# ============================

class AdminParkingLotsResource(Resource):

    # Helper function: check occupancy based on reservations
    def is_spot_occupied(self, spot_id, date, timeslot_id):

        # No date or timeslot = do NOT filter
        if not date or not timeslot_id:
            return False

        pub = PublicReservation.query.filter_by(
            spot_id=spot_id,
            date_of_parking=date,
            timeslot_id=timeslot_id
        ).first()

        if pub:
            return True

        priv = PrivateReservation.query.filter_by(
            spot_id=spot_id,
            date_of_parking=date,
            timeslot_id=timeslot_id
        ).first()

        return priv is not None


    def get(self):
        """
        Returns PUBLIC (non-private) parking lots.
        Supports filtering:
        /admin/parking-lots?date=YYYY-MM-DD&timeslot_id=2
        """

        # Read filters
        date_str = request.args.get("date")
        timeslot_id = request.args.get("timeslot_id", type=int)

        selected_date = None
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                return {"message": "Invalid date format"}, 400

        # Search filter
        query = request.args.get('q', '').strip()
        if query:
            search = f"%{query}%"
            parking_lots = ParkingLot.query.filter(
                ParkingLot.prime_location_name.ilike(search),
                ParkingLot.is_private == False
            ).all()
        else:
            parking_lots = ParkingLot.query.filter_by(is_private=False).all()

        lots_data = []

        # Build response for each lot
        for lot in parking_lots:
            total = lot.max_spots

            # Edge case: empty lot
            if total <= 0:
                lots_data.append({
                    "id": lot.id,
                    "prime_location_name": lot.prime_location_name,
                    "max_spots": 0,
                    "occupied_count": 0,
                    "colored_spots": []
                })
                continue

            # Distribution: 60% normal, 30% extra, 10% VIP
            normal_count = int(0.6 * total)
            extra_count = int(0.3 * total)
            vip_count = int(0.1 * total)

            assigned = normal_count + extra_count + vip_count
            remainder = total - assigned
            extra_count += remainder  # add remainder to extra

            colored_spots = []

            for idx, spot in enumerate(lot.spots):

                # ----- Determine COLOR -----
                if idx < normal_count:
                    color = 'green'
                elif idx < normal_count + extra_count:
                    color = 'grey'
                else:
                    color = 'pink'

                # ----- Determine OCCUPANCY -----
                if selected_date and timeslot_id:
                    occupied = self.is_spot_occupied(
                        spot.id, selected_date, timeslot_id
                    )
                    status = 'O' if occupied else 'A'
                else:
                    status = spot.status

                colored_spots.append({
                    "id": spot.id,
                    "status": status,
                    "color": color
                })

            # Count occupied
            if selected_date and timeslot_id:
                occupied_count = sum(
                    1 for s in lot.spots
                    if self.is_spot_occupied(s.id, selected_date, timeslot_id)
                )
            else:
                occupied_count = sum(
                    1 for s in lot.spots if s.status == 'O'
                )

            lots_data.append({
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "max_spots": total,
                "occupied_count": occupied_count,
                "colored_spots": colored_spots
            })

        return lots_data, 200



    def post(self):
        """
        Create a new parking lot.
        """
        data = request.get_json() or {}

        prime_location_name = data.get("prime_location_name")
        address = data.get("address")
        pin_code = data.get("pin_code")
        price_per_hour = data.get("price_per_hour")
        max_spots = data.get("max_spots")

        # basic validation
        if not all([prime_location_name, address, pin_code, price_per_hour, max_spots]):
            return {"message": "All fields are required."}, 400

        try:
            pin_code = int(pin_code)
            max_spots = int(max_spots)
            price_per_hour = float(price_per_hour)
        except ValueError:
            return {"message": "Invalid numeric value(s)."}, 400

        if max_spots <= 0:
            return {"message": "Max spots must be positive."}, 400

        new_lot = ParkingLot(
            prime_location_name=prime_location_name,
            address=address,
            pin_code=pin_code,
            price_per_hour=price_per_hour,
            max_spots=max_spots,
            is_private=False
        )

        db.session.add(new_lot)
        db.session.flush()  # Get ID before commit

        # Create spot rows
        for _ in range(max_spots):
            spot = ParkingSpot(
                lot_id=new_lot.id,
                status='A'
            )
            db.session.add(spot)

        db.session.commit()

        return {
            "message": "Parking lot created successfully.",
            "lot": {
                "id": new_lot.id,
                "prime_location_name": new_lot.prime_location_name,
                "address": new_lot.address,
                "pin_code": new_lot.pin_code,
                "price_per_hour": new_lot.price_per_hour,
                "max_spots": new_lot.max_spots,
                "is_private": new_lot.is_private
            }
        }, 201



class AdminParkingLotResource(Resource):
    def delete(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"message": "Parking lot not found"}, 404

        db.session.delete(lot)
        db.session.commit()

        return {"message": "Parking lot deleted successfully"}, 200



class AdminSpotResource(Resource):

    def get(self, spot_id):
        """
        Returns individual spot data (no changes needed here).
        """

        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {"message": "Spot not found"}, 404

        lot = spot.lot
        total = lot.max_spots

        normal_count = int(0.6 * total)
        extra_count = int(0.3 * total)
        vip_count = int(0.1 * total)
        assigned = normal_count + extra_count + vip_count
        remainder = total - assigned
        extra_count += remainder

        spots_list = list(lot.spots)
        index = spots_list.index(spot)

        if index < normal_count:
            color = 'green'
        elif index < normal_count + extra_count:
            color = 'grey'
        else:
            color = 'pink'

        return {
            "spot": {
                "id": spot.id,
                "status": spot.status,
                "color": color,
                "lot_id": lot.id
            },
            "lot": {
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "is_private": lot.is_private
            }
        }, 200


    def delete(self, spot_id):
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {"message": "Spot not found"}, 404

        if spot.status != 'A':
            return {
                "message": "Cannot delete: This spot is currently occupied."
            }, 400

        lot = spot.lot
        lot.max_spots -= 1
        db.session.delete(spot)
        db.session.commit()

        return {"message": "Spot deleted successfully."}, 200



# NEW ENDPOINT: Return all time slots for dropdown
class AdminTimeSlotResource(Resource):
    def get(self):
        slots = ParkingTimeSlot.query.all()

        return [
            {
                "id": slot.id,
                "start_time": slot.start_time.strftime("%H:%M"),
                "end_time": slot.end_time.strftime("%H:%M")
            }
            for slot in slots
        ], 200



# Register API routes
api.add_resource(AdminParkingLotsResource, "/admin/parking-lots")
api.add_resource(AdminParkingLotResource, "/admin/parking-lots/<int:lot_id>")
api.add_resource(AdminSpotResource, '/admin/spots/<int:spot_id>')
api.add_resource(AdminTimeSlotResource, "/admin/time-slots")


class FestivalListResource(Resource):
    def get(self):
        # Static list abhi ke liye; baad me DB se bhi de sakte hain
        festivals_list = [
            {"name": "Lohri", "date": "2025-01-13", "density": "Medium"},
            {"name": "Makar Sankranti/Pongal", "date": "2025-01-14", "density": "Medium"},
            {"name": "Vasant Panchami", "date": "2025-02-02", "density": "Medium"},
            {"name": "Maha Shivratri", "date": "2025-02-26", "density": "Medium"},
            {"name": "Holika Dahan", "date": "2025-03-13", "density": "High"},
            {"name": "Holi", "date": "2025-03-14", "density": "High"},
            {"name": "Hindi New Year", "date": "2025-03-20", "density": "High"},
            {"name": "Ugadi", "date": "2025-03-30", "density": "High"},
            {"name": "Ram Navami", "date": "2025-04-06", "density": "Medium"},
            {"name": "Hanuman Jayanti", "date": "2025-04-12", "density": "Medium"},
            {"name": "Vaisakhi", "date": "2025-04-14", "density": "Medium"},
            {"name": "Akshaya Tritiya", "date": "2025-04-30", "density": "Medium"},
            {"name": "Buddha Purnima", "date": "2025-05-12", "density": "High"},
            {"name": "Savitri Pooja", "date": "2025-05-26", "density": "Medium"},
            {"name": "Puri Rath Yatra", "date": "2025-06-27", "density": "Low"},
            {"name": "Guru Purnima", "date": "2025-07-10", "density": "Medium"},
            {"name": "Sawan Shivratri", "date": "2025-07-23", "density": "High"},
            {"name": "Hariyali Teej", "date": "2025-07-27", "density": "Medium"},
            {"name": "Nag Panchami", "date": "2025-07-29", "density": "Medium"},
            {"name": "Varalakshmi Vrat", "date": "2025-08-08", "density": "High"},
            {"name": "Raksha Bandhan", "date": "2025-08-09", "density": "High"},
            {"name": "Krishna Janmashtami", "date": "2025-08-15", "density": "High"},
            {"name": "Hartalika Teej", "date": "2025-08-26", "density": "High"},
            {"name": "Ganesh Chaturthi", "date": "2025-08-27", "density": "High"},
            {"name": "Onam", "date": "2025-09-05", "density": "Medium"},
            {"name": "Navaratri Begins", "date": "2025-09-22", "density": "Medium"},
            {"name": "Navaratri Ends", "date": "2025-10-01", "density": "High"},
            {"name": "Dussehra", "date": "2025-10-02", "density": "High"},
            {"name": "Gandhi Jayanti", "date": "2025-10-02", "density": "High"},
            {"name": "Sharad Purnima", "date": "2025-10-06", "density": "High"},
            {"name": "Karwa Chauth", "date": "2025-10-10", "density": "High"},
            {"name": "Dhan Teras", "date": "2025-10-18", "density": "High"},
            {"name": "Diwali", "date": "2025-10-20", "density": "High"},
            {"name": "Bhai Dooj", "date": "2025-10-23", "density": "High"},
            {"name": "Chhath Puja", "date": "2025-10-27", "density": "High"},
            {"name": "Kartik Poornima", "date": "2025-11-05", "density": "Low"},
            {"name": "Geeta Jayanti", "date": "2025-12-01", "density": "Low"},
            {"name": "Dhanu Sankranti", "date": "2025-12-16", "density": "Low"},
            {"name": "Christmas", "date": "2025-12-25", "density": "Low"}
        ]
        return {"festivals": festivals_list}, 200
api.add_resource(FestivalListResource, '/festivals')
#added
class AdminPrivateParkingLotsResource(Resource):
    def get(self):
        """Return private lots + spot occupancy for selected date & timeslot."""
        date_str = request.args.get("date")
        timeslot_id = request.args.get("timeslot_id")

        selected_date = None
        if date_str:
            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400

        private_lots = ParkingLot.query.filter_by(is_private=True).all()
        lots_data = []

        for lot in private_lots:
            spots_sorted = sorted(lot.spots, key=lambda s: s.id)
            spots_data = []
            occupied_count = 0

            for spot in spots_sorted:

                # Default available
                status = "A"

                # If date + timeslot selected, check if reservation exists
                if selected_date and timeslot_id:
                    reservation = PrivateReservation.query.filter_by(
                        spot_id=spot.id,
                        date_of_parking=selected_date,
                        timeslot_id=timeslot_id
                    ).first()

                    if reservation:
                        status = "O"

                # Count only within selected filter
                if status == "O":
                    occupied_count += 1

                spots_data.append({
                    "id": spot.id,
                    "status": status
                })

            lots_data.append({
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "max_spots": lot.max_spots,
                "occupied_count": occupied_count,
                "spots": spots_data
            })

        return lots_data, 200

class AdminPrivateLotResource(Resource):
    def delete(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot or not lot.is_private:
            return {"message": "Private lot not found"}, 404

        # Delete all spots of this lot too
        for spot in list(lot.spots):
            db.session.delete(spot)

        db.session.delete(lot)
        db.session.commit()
        return {"message": "Private parking lot deleted successfully."}, 200
api.add_resource(AdminPrivateParkingLotsResource, '/admin/private-parking-lots')
api.add_resource(AdminPrivateLotResource, '/admin/private-parking-lots/<int:lot_id>')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
class ScanTicketImageResource(Resource):
    def post(self):
        """
        Handle QR image upload, decode ticket id, and update ticket status/scan_count.
        Mirrors the logic of the Jinja /scan-ticket route.
        """
        ticket = None

        file = request.files.get('qr_image')
        if not file or file.filename == '':
            return {
                "success": False,
                "message": "❌ No image uploaded."
            }, 400

        try:
            # Save file (same pattern as original)
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            print(filepath)
            img = cv2.imread(filepath)

            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(img)

            if data:
                try:
                    decoded = Base64.b64decode(data).decode("utf-8")
                except Exception:
                    decoded = data
                print(decoded)
            else:
                return {
                    "success": False,
                    "message": "❌ Could not read QR code."
                }, 400
            # # Open and decode
            # img = Image.open(filepath)
            # print(type(img))
            # decoded_objs = decode(img)
            # print(decoded_objs)
            # print(type(decoded_objs[0]))
            # if decoded_objs:
            #     qr_data = decoded_objs[0].data
            #     decoded = Base64.b64decode(qr_data).decode("utf-8")
            #     print(decoded)
            #     print(type(decoded))
            # else:
            #     return {
            #         "success": False,
            #         "message": "❌ Could not read QR code from uploaded file."
            #     }, 400

            # Interpret QR content as ticket_id
            try:
                data = ast.literal_eval(decoded)
                passenger_id=data['passenger_id']
                print(passenger_id)
                print(type(passenger_id))
            except :
                print("kutta bacha")
                return {
                    "success": False,
                    "message": "❌ Invalid QR code content."
                }, 400

            ticket = Passenger.query.get(passenger_id)
            if not ticket:
                return {
                    "success": False,
                    "message": "❌ Ticket not found."
                }, 404

            # Same logic as your original route
            if ticket.scan_count == 0:
                ticket.scan_count = 1
                message = f"✅ Entry granted for Ticket {ticket.id}"
            elif ticket.scan_count == 1:
                ticket.scan_count = 2
                message = f"✅ Exit recorded for Ticket {ticket.id}"
            else:
                message = f"❌ Ticket {ticket.id} already expired."

            db.session.commit()

            return {
                "success": True,
                "message": message,
                "ticket": {
                    "id": ticket.id,
                    "scan_count": ticket.scan_count,
                },
            }, 200

        except Exception as e:
            # Generic error fallback
            return {
                "success": False,
                "message": f"❌ Error processing image: {e}"
            }, 500

class ScanTicketLiveResource(Resource):
    """
    Expect POST JSON: { "qr_text": "<base64-or-raw-string-from-QR>" }
    The client (browser) should decode QR and send the QR payload to this endpoint.
    """
    def post(self):
        payload = None
        try:
            data = request.get_json(force=True, silent=True) or {}
            qr_text = data.get("qr_text")
            if not qr_text:
                return {"success": False, "message": "❌ No QR text provided."}, 400

            # qr_text may be bytes-string or str; if it looks base64, decode it
            decoded_str = None
            try:
                # If qr_text is bytes-like inside string, ensure bytes
                if isinstance(qr_text, str):
                    qr_bytes = qr_text.encode("utf-8")
                else:
                    qr_bytes = qr_text

                # Try base64 decode first (most of your QRs contain base64-encoded dict)
                try:
                    decoded_str = Base64.b64decode(qr_bytes).decode("utf-8")
                except Exception:
                    # fallback: maybe it's already a plain string dict not base64
                    decoded_str = qr_text if isinstance(qr_text, str) else qr_text.decode("utf-8")
            except Exception as e:
                return {"success": False, "message": f"❌ Failed to normalize QR text: {e}"}, 400

            # parse the string into python dict safely
            try:
                parsed = ast.literal_eval(decoded_str)
                passenger_id = parsed.get("passenger_id")
                if passenger_id is None:
                    raise ValueError("passenger_id missing in QR payload")
            except Exception as e:
                return {"success": False, "message": f"❌ Invalid QR payload: {e}"}, 400

            # retrieve ticket
            try:
                ticket = Passenger.query.get(int(passenger_id))
            except Exception as e:
                return {"success": False, "message": f"❌ Invalid passenger_id: {e}"}, 400

            if not ticket:
                return {"success": False, "message": "❌ Ticket not found."}, 404

            # Same logic as static scan
            if ticket.scan_count == 0:
                ticket.scan_count = 1
                message = f"✅ Entry granted for Ticket {ticket.id}"
            elif ticket.scan_count == 1:
                ticket.scan_count = 2
                message = f"✅ Exit recorded for Ticket {ticket.id}"
            else:
                message = f"❌ Ticket {ticket.id} already expired."

            db.session.commit()

            return {
                "success": True,
                "message": message,
                "ticket": {
                    "id": ticket.id,
                    "scan_count": ticket.scan_count,
                },
            }, 200

        except Exception as e:
            return {"success": False, "message": f"❌ Server error: {e}"}, 500

api.add_resource(ScanTicketImageResource, '/scan-ticket/image')
api.add_resource(ScanTicketLiveResource, '/scan-ticket/live')

class AdminSummaryResource(Resource):
    def get(self):
        """
        Return summary stats for admin analytics dashboard.
        This mirrors the logic from the Jinja `summary` route.
        """
        parking_lots = ParkingLot.query.filter_by(is_private=False).all()

        lot_names = []
        revenues = []
        total_spots = 0
        occupied_spots = 0
        total_revenue = 0

        for lot in parking_lots:
            lot_names.append(lot.prime_location_name)

            # Example logic – yahan tum apna actual revenue calc daalna:
            # Assume lot has relationship `reservations` or `tickets` etc.
            lot_revenue = 0
            # for r in lot.reservations:
            #     lot_revenue += r.amount
            #
            # For now, we try attribute:
            if hasattr(lot, "total_revenue") and lot.total_revenue is not None:
                lot_revenue = lot.total_revenue

            revenues.append(lot_revenue)
            total_revenue += lot_revenue

            # Spot counts
            spots_list = list(lot.spots)
            total_spots += len(spots_list)
            occupied_spots += sum(1 for s in spots_list if s.status == 'O')

        vacant_spots = max(total_spots - occupied_spots, 0)

        return {
            "lot_names": lot_names,
            "revenues": revenues,
            "total_spots": total_spots,
            "occupied_spots": occupied_spots,
            "vacant_spots": vacant_spots,
            "total_revenue": total_revenue
        }, 200
api.add_resource(AdminSummaryResource, '/admin/summary')

class AdminUsersResource(Resource):
    def get(self):
        users = User.query.filter_by(role=1).all()  # or filter by user role if required
        return [
            {
                "id": u.id,
                "email": u.email,
                "name": u.name,
                "address": u.address,
                "pincode": u.pincode,
            }
            for u in users
        ], 200

api.add_resource(AdminUsersResource, '/admin/users')


class BooksevaResource(Resource):
    def get(self,user_id):
        bookings = User.query.filter_by(id=user_id).first()
        return {
                "email": bookings.email,
                "mobile_no": bookings.mobile_no,
                "name": bookings.name,
            }, 200

    def post(self,user_id=None):
        data = request.get_json()
        user_id = data.get("user_id")
        seva_name = data.get("seva_name")
        seva_date_str = data.get("seva_date")
        participants = data.get("num_people")

        if not all([user_id, seva_name, seva_date_str, participants]):
            return {"success": False, "message": "All fields are required."}, 400

        try:
            seva_date = datetime.strptime(seva_date_str, "%Y-%m-%d").date()
        except ValueError:
            return {"success": False, "message": "Invalid date format."}, 400

        new_seva_booking = SevaBooking(
            user_id=user_id,
            seva_name=seva_name,
            booking_date=seva_date,
            quantity=participants
        )

        db.session.add(new_seva_booking)
        db.session.commit()
        response_data = {
                "id": new_seva_booking.id,
                "user_id": new_seva_booking.user_id,
                "seva_name": new_seva_booking.seva_name,
                "seva_date": new_seva_booking.booking_date.strftime("%Y-%m-%d"),
                "participants": new_seva_booking.quantity}
        qrgenerator(str(response_data),f"seva_booking_{new_seva_booking.id}.png")
        
        
        TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=f"Seva '{seva_name}' booked in the name of {new_seva_booking.user.name} on {seva_date_str} for {participants} participants.",
                    media_url=[f"{clouflare_url}/api/qrcode/seva_booking_{new_seva_booking.id}.png"],
                    to=f"whatsapp:+91{new_seva_booking.user.mobile_no}"
                    )
        return {
            "success": True,
            "message": "Seva booked successfully."}, 201

api.add_resource(BooksevaResource, '/book-seva/<int:user_id>')


class AdminDarshanslotResource(Resource):

    def get(self):
        param_type = request.args.get('type')
        slots = Aarti_and_DarshanSlot.query.filter_by(slot_type=param_type).order_by(Aarti_and_DarshanSlot.start_time).all()

        return [
            {
                "id": s.id,
                "start_time": s.start_time.strftime("%H:%M"),
                "end_time": s.end_time.strftime("%H:%M"),
                "max_visitors": s.max_visitors
            }
            for s in slots
        ], 200

    def post(self):
        data = request.get_json()
        slot_type = data.get("slot_type")
        start_time_str = data.get("start_time")
        end_time_str = data.get("end_time")
        max_visitors = data.get("max_visitors")

        if not all([slot_type, start_time_str, end_time_str, max_visitors]):
            return {"message": "All fields are required."}, 400

        try:
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
            max_visitors = int(max_visitors)
        except ValueError:
            return {"message": "Invalid time format or max visitors."}, 400

        new_slot = Aarti_and_DarshanSlot(
            slot_type=slot_type,
            start_time=start_time,
            end_time=end_time,
            max_visitors=max_visitors
        )

        db.session.add(new_slot)
        db.session.commit()

        return {
            "message": "Slot created successfully.",
            "slot": {
                "id": new_slot.id,
                "slot_type": new_slot.slot_type,
                "start_time": new_slot.start_time.strftime("%H:%M"),
                "end_time": new_slot.end_time.strftime("%H:%M"),
                "max_visitors": new_slot.max_visitors
            }
        }, 201

    def put(self):
        data = request.get_json()
        slot_id = data.get("id")

        slot = Aarti_and_DarshanSlot.query.get(slot_id)
        if not slot:
            return {"message": "Slot not found."}, 404

        try:
            if "start_time" in data:
                slot.start_time = datetime.strptime(data["start_time"], "%H:%M").time()
            if "end_time" in data:
                slot.end_time = datetime.strptime(data["end_time"], "%H:%M").time()
            if "max_visitors" in data:
                slot.max_visitors = int(data["max_visitors"])
        except ValueError:
            return {"message": "Invalid data format."}, 400

        db.session.commit()

        return {"message": "Slot updated successfully."}, 200

    def delete(self):
        slot_id = request.args.get("id")
        slot = Aarti_and_DarshanSlot.query.get(slot_id)

        if not slot:
            return {"message": "Slot not found."}, 404

        db.session.delete(slot)
        db.session.commit()

        return {"message": "Slot deleted."}, 200
api.add_resource(AdminDarshanslotResource, '/admin/darshan-slots')


class ParkingLotResource(Resource):
    def get(self):
        lot_type = request.args.get("type")  # 'public' or 'private'

        query = ParkingLot.query
        if lot_type == "public":
            query = query.filter_by(is_private=False)
        elif lot_type == "private":
            query = query.filter_by(is_private=True)

        lots = query.all()

        return {
            "lots": [
                {
                    "id": lot.id,
                    "name": lot.prime_location_name,
                    "address": lot.address,
                    "pin_code": lot.pin_code,
                    "price_per_hour": lot.price_per_hour,
                    "max_spots": lot.max_spots,
                    "is_private": lot.is_private
                }
                for lot in lots
            ]
        }, 200

api.add_resource(ParkingLotResource, '/parking-lots')

class ParkingTimeSlotsResource(Resource):
    def get(self):
        slots = ParkingTimeSlot.query.order_by(ParkingTimeSlot.start_time).all()
        
        return {
            "slots": [
                {
                    "id": slot.id,
                    "start_time": slot.start_time.strftime("%H:%M"),
                    "end_time": slot.end_time.strftime("%H:%M"),
                    "slot_order": i + 1,  # derived order
                }
                for i, slot in enumerate(slots)
            ]
        }, 200
api.add_resource(ParkingTimeSlotsResource,'/parking-time-slots')

class BookParking(Resource):
    def post(self):
        data = request.get_json()

        user_id = data.get("user_id")
        lot_id = data.get("lot_id")
        vehicle = data.get("vehicle_number")
        date = data.get("parking_date")

        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"message": "Invalid parking lot"}, 400

        # PUBLIC BOOKING -----------------------------------------------------
        if not lot.is_private:
            slot_id = data.get("slot_id")

            # Try to find an available spot
            spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()

            for spot in spots:
                exists = PublicReservation.query.filter_by(
                    spot_id=spot.id,
                    date_of_parking=date,
                    timeslot_id=slot_id
                ).first()

                if not exists:
                    # Book this spot
                    res = PublicReservation(
                        lot_id=lot_id,
                        spot_id=spot.id,
                        user_id=user_id,
                        vehicle_number=vehicle,
                        date_of_parking=datetime.strptime(date, "%Y-%m-%d"),
                        timeslot_id=slot_id
                    )
                    db.session.add(res)
                    db.session.commit()

                    return {"message": "Public parking booked successfully!"}, 200
            
            return {"message": "No available spots for this time slot"}, 409

        # PRIVATE BOOKING -----------------------------------------------------
        else:
            start_slot = data.get("start_slot")
            end_slot = data.get("end_slot")

            if not start_slot or not end_slot:
                return {"message": "Provide start and end slot"}, 400

            # Ensure ordered correctly
            if start_slot > end_slot:
                return {"message": "End slot must be after start slot"}, 400

            # Get the slot range
            full_range = ParkingTimeSlot.query.filter(
                ParkingTimeSlot.id >= start_slot,
                ParkingTimeSlot.id <= end_slot
            ).all()

            # Try to find spot where ALL slots are free
            spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()

            for spot in spots:
                conflict = PrivateReservation.query.filter(
                    PrivateReservation.spot_id == spot.id,
                    PrivateReservation.date_of_parking == date,
                    PrivateReservation.timeslot_id.in_([s.id for s in full_range])
                ).first()

                if not conflict:
                    # Reserve all slots individually
                    for s in full_range:
                        r = PrivateReservation(
                            lot_id=lot_id,
                            spot_id=spot.id,
                            user_id=user_id,
                            vehicle_number=vehicle,
                            date_of_parking=datetime.strptime(date, "%Y-%m-%d"),
                            timeslot_id=s.id
                        )
                        db.session.add(r)

                    db.session.commit()
                    return {"message": "Private parking booked successfully!"}, 200

            return {"message": "No spot available for the requested time range"}, 409
api.add_resource(BookParking,'/book-parking')


class SlotAvailabilityResource(Resource):
    def get(self):
        slot_type = request.args.get('type')
        date_str = request.args.get('date')  # yyyy-mm-dd format

        if not slot_type:
            return {"message": "Slot type required"}, 400

        if not date_str:
            return {"message": "Date required"}, 400

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return {"message": "Invalid date format, must be YYYY-MM-DD"}, 400

        # Fetch all slots of this type (Aarti or Darshan)
        slots = Aarti_and_DarshanSlot.query.filter_by(slot_type=slot_type).all()

        results = []

        for slot in slots:
            # Count passengers for this slot on that date
            booked_count = Passenger.query.filter_by(
                slot_id=slot.id,
                darshan_date=selected_date
            ).count()

            results.append({
                "slot_id": slot.id,
                "slot_type": slot.slot_type,
                "start": slot.start_time.strftime("%H:%M"),
                "end": slot.end_time.strftime("%H:%M"),
                "capacity": slot.max_visitors,
                "booked": booked_count,
                "available": slot.max_visitors - booked_count
            })

        return {"slots": results}, 200


api.add_resource(SlotAvailabilityResource, "/slots")
