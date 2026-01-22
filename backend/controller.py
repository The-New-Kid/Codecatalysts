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
from werkzeug.security import generate_password_hash, check_password_hash
from gittest import super
from crowd_model import predict_crowd_for_date
from twilio.twiml.voice_response import VoiceResponse, Gather

load_dotenv()
CURRENT_COUNT_MANDIR=0
MAX_COUNT_MANDIR=1
MIN_COUNT_MADIR=0
FLAG=0
api=Api(prefix='/api')
otp_login_storage = {}
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
CONTENT_SID = os.getenv("CONTENT_SID")
clouflare_url=os.getenv("PUBLIC_BASE_URL")
TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

IVR_TWILIO_SID = os.getenv("IVR_TWILIO_SID")
IVR_AUTH_TOKEN = os.getenv("IVR_AUTH_TOKEN")
IVR_NUMBER = os.getenv("IVR_NUMBER")

IVR_CLIENT = Client(IVR_TWILIO_SID, IVR_AUTH_TOKEN, IVR_NUMBER)

SMS_SID = os.getenv("SMS_SID")
SMS_TOKEN = os.getenv("SMS_TOKEN")
SMS_NUMBER = os.getenv("SMS_NUMBER")

SMS_CLIENT = Client(SMS_SID, SMS_TOKEN, SMS_NUMBER)

SECURITY_OFFICER = "+917456097831"
SHUTTLE_BUS = "6396526619"

AADHAR_MOBILE_MAP = {
    "111122223333": "+917042213383",#shivang
    "222233334444": "+916396081309",#vansh
    "333344445555": "+919696733181",#priyanshu
    "444455556666": "+917456097831",#srashti
    "555566667777": "+916396526619",#Ayush
    "666677778888": "+916389890800",#tushar
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

        if not check_password_hash(user.password, password):
            return {"message": "Incorrect password"}, 401

        role = "admin" if user.role == 0 else "user"

        return {
            "message": "Login successful",
            "user_id": user.id,
            "role": role,
            "name": user.name
        }, 200
api.add_resource(LoginResource,'/login')

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        pincode = data.get('pincode')
        address = data.get('address')
        mobile_no = data.get('mobile_no')

        email = email.lower()

        if not all([name, email, password, pincode, address, mobile_no]):
            return {"message": "All fields are required"}, 400

        # Check duplicate
        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered"}, 409
        if User.query.filter_by(mobile_no=mobile_no).first():
            return {"message": "Mobile number already registered"}, 409

        # Encrypt that secret
        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            pincode=pincode,
            address=address,
            mobile_no=mobile_no
        )

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
        passengers = data.get("passengers", [])
        mobile_number = data.get("booker_mobile") or data.get("mobile_number")

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

        already_booked = Passenger.query.filter_by(
            slot_id=slot_id,
            darshan_date=selected_date
        ).count()

        if already_booked + num_members > slot.max_visitors:
            return {
                "success": False,
                "message": f"Only {slot.max_visitors - already_booked} slots left"
            }, 400

        # QR Setup
        QR_FOLDER = os.path.join("static", "qrcode")
        os.makedirs(QR_FOLDER, exist_ok=True)

        booked_passengers = []
        special_priority_map = []

        # 1st PASS: assign priority for special passengers
        for p in passengers:
            if not p.get("is_special"):
                special_priority_map.append(None)
                continue

            age = int(p.get("age", 0))
            wheelchair_needed = p.get("wheelchair_needed", False)

            # Base priority rules
            priority = 0
            if 60 <= age < 70:
                priority += 1
            elif age >= 70:
                priority += 2
            if wheelchair_needed:
                priority += 4

            special_priority_map.append(priority)

        # Extract priorities of only specials in original order
        special_priorities = [pr for pr in special_priority_map if pr is not None]
        special_index = 0

        # 2nd PASS: save passengers and assign priority
        for idx, p in enumerate(passengers):
            name = p.get("name")
            aadhar = p.get("aadhar")
            otp_entered = p.get("otp", None)

            if otp_storage.get(aadhar) != otp_entered:
                return {"success": False, "message": f"OTP failed for {name}"}, 400
            otp_storage.pop(aadhar, None)

            age = int(p.get("age", 0))
            gender = p.get("gender", "")

            is_special = p.get("is_special", False)
            with_special = p.get("with_special", False)
            wheelchair_needed = p.get("wheelchair_needed", False)

            if is_special:
                priority = special_priorities[special_index]
                special_index += 1
            else:
                # Assign accompanying priority = special counterpart
                if with_special and special_priorities:
                    priority = special_priorities[0]  # Link to first special
                else:
                    priority = 0

            passenger = Passenger(
                user_id=user.id,
                slot_id=slot.id,
                darshan_date=selected_date,
                name=name,
                special=is_special,
                with_special=with_special,
                aadhaar_number=aadhar,
                age=age,
                gender=gender,
                priority=priority,
                wheelchairneeded=wheelchair_needed
            )
            db.session.add(passenger)
            db.session.flush()

            qr_data = str({
                "name": name,
                "passenger_id": passenger.id,
                "darshan_date": darshan_date,
                "slot_id": slot_id,
                "aadhar": aadhar,
                "special": is_special,
                "with_special": with_special,
                "priority": priority
            })
            qr_filename = f"passenger_{passenger.id}_{secure_filename(name)}.png"
            encoded = qrgenerator(qr_data, qr_filename)
            passenger.qr_code = encoded

            slot_type = passenger.slot.slot_type
            try:
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=f"{slot_type} Ticket #{passenger.id} booked for {name}",
                    media_url=[f"{clouflare_url}/api/qrcode/{qr_filename}"],
                    to=f"whatsapp:+91{mobile_number}"
                )
            except Exception as e:
                print("WhatsApp Error:", e)

            booked_passengers.append({
                "passenger_id": passenger.id,
                "qr_code": qr_filename
            })

        db.session.commit()

        return {"success": True, "passengers": booked_passengers}, 200

api.add_resource(BookTicketResource, '/book-ticket')

def find_first_available_slot(slot_type, darshan_date):
    """
    Find the earliest slot of given type (e.g. 'Darshan')
    that still has capacity on the given date.
    """
    slots = Aarti_and_DarshanSlot.query.filter_by(
        slot_type=slot_type
    ).order_by(Aarti_and_DarshanSlot.start_time).all()

    for slot in slots:
        booked = Passenger.query.filter_by(
            slot_id=slot.id,
            darshan_date=darshan_date
        ).count()
        if booked < slot.max_visitors:
            return slot

    return None

def get_ordered_darshan_slots():
    """
    Return all Darshan slots ordered by start_time.
    Used by IVR slot selection.
    """
    return Aarti_and_DarshanSlot.query.filter_by(
        slot_type="Darshan"
    ).order_by(Aarti_and_DarshanSlot.start_time).all()

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
        month = int(data["month"])
        year = int(data["year"])

        print(type(month), type(year))

        # 1) Get festivals for this month/year
        list_hindu = super(year=str(year), month=month) or []
        print("festivals list:", list_hindu)

        # {day: fest_name}
        festival_map = {}
        for item in list_hindu:
            try:
                d = int(item.get("date"))
                n = item.get("name")
                if d and n:
                    festival_map[d] = n
            except Exception:
                pass

        total_days = calendar.monthrange(year, month)[1]
        print("fest map:", festival_map)
        result = {}

        for day in range(1, total_days + 1):
            fest = festival_map.get(day)  # could be None
            # for ML model, use "Normal" if no fest
            fest_label = fest if fest else "Normal"

            cached = PanchangCache.query.filter_by(
                day=day, month=month, year=year
            ).first()

            if cached and cached.tithi and cached.crowd is not None:
                # ✅ return cached data
                result[day] = {
                    "tithi": cached.tithi,
                    "fest": cached.fest,
                    "crowd": cached.crowd
                }
                continue

            # ---------- Call external Panchang API ----------
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
            resp_json = response.json()
            tithi = resp_json.get("tithi")

            # ---------- Predict crowd for this day ----------
            try:
                crowd_pred = predict_crowd_for_date(
                    year=year,
                    month=month,
                    day=day,
                    festival_label=fest_label
                )
            except Exception as e:
                print(f"[ML ERROR] {year}-{month}-{day}: {e}")
                crowd_pred = None

            # ---------- Save to cache ----------
            if cached:
                cached.tithi = tithi
                cached.fest = fest
                cached.crowd = crowd_pred
            else:
                new_entry = PanchangCache(
                    day=day,
                    month=month,
                    year=year,
                    tithi=tithi,
                    fest=fest,
                    crowd=crowd_pred
                )
                db.session.add(new_entry)

            db.session.commit()

            result[day] = {
                "tithi": tithi,
                "fest": fest,
                "crowd": crowd_pred
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


# class FestivalListResource(Resource):
#     def get(self):
#         # Static list abhi ke liye; baad me DB se bhi de sakte hain
#         festivals_list = [
#             {"name": "Lohri", "date": "2025-01-13", "density": "Medium"},
#             {"name": "Makar Sankranti/Pongal", "date": "2025-01-14", "density": "Medium"},
#             {"name": "Vasant Panchami", "date": "2025-02-02", "density": "Medium"},
#             {"name": "Maha Shivratri", "date": "2025-02-26", "density": "Medium"},
#             {"name": "Holika Dahan", "date": "2025-03-13", "density": "High"},
#             {"name": "Holi", "date": "2025-03-14", "density": "High"},
#             {"name": "Hindi New Year", "date": "2025-03-20", "density": "High"},
#             {"name": "Ugadi", "date": "2025-03-30", "density": "High"},
#             {"name": "Ram Navami", "date": "2025-04-06", "density": "Medium"},
#             {"name": "Hanuman Jayanti", "date": "2025-04-12", "density": "Medium"},
#             {"name": "Vaisakhi", "date": "2025-04-14", "density": "Medium"},
#             {"name": "Akshaya Tritiya", "date": "2025-04-30", "density": "Medium"},
#             {"name": "Buddha Purnima", "date": "2025-05-12", "density": "High"},
#             {"name": "Savitri Pooja", "date": "2025-05-26", "density": "Medium"},
#             {"name": "Puri Rath Yatra", "date": "2025-06-27", "density": "Low"},
#             {"name": "Guru Purnima", "date": "2025-07-10", "density": "Medium"},
#             {"name": "Sawan Shivratri", "date": "2025-07-23", "density": "High"},
#             {"name": "Hariyali Teej", "date": "2025-07-27", "density": "Medium"},
#             {"name": "Nag Panchami", "date": "2025-07-29", "density": "Medium"},
#             {"name": "Varalakshmi Vrat", "date": "2025-08-08", "density": "High"},
#             {"name": "Raksha Bandhan", "date": "2025-08-09", "density": "High"},
#             {"name": "Krishna Janmashtami", "date": "2025-08-15", "density": "High"},
#             {"name": "Hartalika Teej", "date": "2025-08-26", "density": "High"},
#             {"name": "Ganesh Chaturthi", "date": "2025-08-27", "density": "High"},
#             {"name": "Onam", "date": "2025-09-05", "density": "Medium"},
#             {"name": "Navaratri Begins", "date": "2025-09-22", "density": "Medium"},
#             {"name": "Navaratri Ends", "date": "2025-10-01", "density": "High"},
#             {"name": "Dussehra", "date": "2025-10-02", "density": "High"},
#             {"name": "Gandhi Jayanti", "date": "2025-10-02", "density": "High"},
#             {"name": "Sharad Purnima", "date": "2025-10-06", "density": "High"},
#             {"name": "Karwa Chauth", "date": "2025-10-10", "density": "High"},
#             {"name": "Dhan Teras", "date": "2025-10-18", "density": "High"},
#             {"name": "Diwali", "date": "2025-10-20", "density": "High"},
#             {"name": "Bhai Dooj", "date": "2025-10-23", "density": "High"},
#             {"name": "Chhath Puja", "date": "2025-10-27", "density": "High"},
#             {"name": "Kartik Poornima", "date": "2025-11-05", "density": "Low"},
#             {"name": "Geeta Jayanti", "date": "2025-12-01", "density": "Low"},
#             {"name": "Dhanu Sankranti", "date": "2025-12-16", "density": "Low"},
#             {"name": "Christmas", "date": "2025-12-25", "density": "Low"}
#         ]
#         return {"festivals": festivals_list}, 200
# api.add_resource(FestivalListResource, '/festivals')
# #added
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

            try:
                data = ast.literal_eval(decoded)
                passenger_id = data['passenger_id']
                print(passenger_id)
                print(type(passenger_id))
            except:
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

            global CURRENT_COUNT_MANDIR
            global FLAG

            # ----- Crowd / scan logic -----
            if ticket.scan_count == 0 and FLAG == 0:
                # First entry and gate is open
                ticket.scan_count = 1
                CURRENT_COUNT_MANDIR = CURRENT_COUNT_MANDIR + 1
                print("CURRENT_COUNT_MANDIR after entry:", CURRENT_COUNT_MANDIR)
                message = f"✅ Entry granted for Ticket {ticket.id}"

            elif ticket.scan_count == 1:
                # Exit
                ticket.scan_count = 2
                CURRENT_COUNT_MANDIR = max(0, CURRENT_COUNT_MANDIR - 1)
                print("CURRENT_COUNT_MANDIR after exit:", CURRENT_COUNT_MANDIR)
                message = f"✅ Exit recorded for Ticket {ticket.id}"

            elif ticket.scan_count == 2:
                message = f"❌ Ticket {ticket.id} already expired."

            else:
                # scan_count == 0 but FLAG == 1  -> full / gate closed
                message = "❌ Mandir is currently full. Please wait for some time."

            # --- Recalculate gate state, send SMS if gate open/close changed ---
            update_gate_state_and_notify()

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

            global CURRENT_COUNT_MANDIR
            global FLAG

            # ----- Crowd / scan logic -----
            if ticket.scan_count == 0 and FLAG == 0:
                # First entry and gate is open
                ticket.scan_count = 1
                CURRENT_COUNT_MANDIR = CURRENT_COUNT_MANDIR + 1
                print("CURRENT_COUNT_MANDIR after entry:", CURRENT_COUNT_MANDIR)
                message = f"✅ Entry granted for Ticket {ticket.id}"

            elif ticket.scan_count == 1:
                # Exit
                ticket.scan_count = 2
                CURRENT_COUNT_MANDIR = max(0, CURRENT_COUNT_MANDIR - 1)
                print("CURRENT_COUNT_MANDIR after exit:", CURRENT_COUNT_MANDIR)
                message = f"✅ Exit recorded for Ticket {ticket.id}"

            elif ticket.scan_count == 2:
                message = f"❌ Ticket {ticket.id} already expired."

            else:
                # scan_count == 0 but FLAG == 1  -> full / gate closed
                message = "❌ Mandir is currently full. Please wait for some time."

            # --- Recalculate gate state, send SMS if gate open/close changed ---
            update_gate_state_and_notify()

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
api.add_resource(MobileLoginResource, '/mobile-login')
api.add_resource(LoginverifyotpResource, '/login-verify-otp')
api.add_resource(ImageserverResource,'/qrcode/<string:filename>')
api.add_resource(VerifyOtpResource, '/verify-otp')
api.add_resource(SendOtpResource, "/send-otp")

# class TwilioIVRStart(Resource):
#     """
#     Main IVR entry: Twilio Voice webhook -> /api/twilio/voice
#     Configure this URL in Twilio Console for your phone number.
#     """
#     def post(self):
#         resp = VoiceResponse()

#         gather = resp.gather(
#             num_digits=1,
#             action="/api/twilio/menu",
#             method="POST"
#         )
#         gather.say(
#             "Jai Somnath. "
#             "For Sugam Darshan ticket booking, press 1. "
#             "For Sugam Aarti booking, press 2."
#         )

#         # If no input
#         resp.say("Sorry, we did not receive any input. Jai Somnath. Goodbye.")
#         return make_response(str(resp), 200, {"Content-Type": "text/xml"})
    
# class TwilioIVRMenu(Resource):
#     def post(self):
#         resp = VoiceResponse()
#         digits = request.values.get("Digits")

#         if digits == "1":
#             # Go to Aadhaar capture for Darshan booking
#             resp.redirect("/api/twilio/aadhar-darshan")
#         elif digits == "2":
#             resp.say("Aarti booking via phone will be available soon. Please use the mobile app or website. Jai Somnath.")
#             resp.hangup()
#         else:
#             resp.say("Invalid choice.")
#             resp.redirect("/api/twilio/voice")

#         return make_response(str(resp), 200, {"Content-Type": "text/xml"})

# class TwilioIVRAadhaarDarshan(Resource):
#     """
#     Ask devotee to enter 12 digit Aadhaar number.
#     Uses the static AADHAR_MOBILE_MAP for demo.
#     """
#     def post(self):
#         resp = VoiceResponse()

#         gather = resp.gather(
#             num_digits=12,
#             action="/api/twilio/aadhar-darshan-verify",
#             method="POST"
#         )
#         gather.say(
#             "Please enter your twelve digit Aadhaar number, "
#             "followed by the hash key."
#         )

#         resp.say("No input received. Restarting.")
#         resp.redirect("/api/twilio/aadhar-darshan")
#         return make_response(str(resp), 200, {"Content-Type": "text/xml"})

# class TwilioIVRAadhaarDarshanVerify(Resource):
#     def post(self):
#         resp = VoiceResponse()
#         aadhar = request.values.get("Digits")

#         if not aadhar:
#             resp.say("Aadhaar number not received. Please try again.")
#             resp.redirect("/api/twilio/aadhar-darshan")
#             return make_response(str(resp), 200, {"Content-Type": "text/xml"})

#         mobile = AADHAR_MOBILE_MAP.get(aadhar)
#         if not mobile:
#             resp.say(
#                 "This Aadhaar is not registered with Dev Dham Path. "
#                 "Please use the app or website to register first. Jai Somnath."
#             )
#             resp.hangup()
#             return make_response(str(resp), 200, {"Content-Type": "text/xml"})

#         # Aadhaar OK → ask date
#         gather = resp.gather(
#             num_digits=1,
#             action=f"/api/twilio/darshan-date?aadhar={aadhar}",
#             method="POST"
#         )
#         gather.say(
#             "For today darshan, press 1. "
#             "For tomorrow darshan, press 2."
#         )

#         resp.say("No input received. Restarting.")
#         resp.redirect(f"/api/twilio/darshan-date?aadhar={aadhar}")
#         return make_response(str(resp), 200, {"Content-Type": "text/xml"})
    
# class TwilioIVRDarshanDate(Resource):
#     def post(self):
#         from datetime import date  # local import is fine

#         resp = VoiceResponse()
#         aadhar = request.args.get("aadhar")
#         choice = request.values.get("Digits")

#         if not aadhar:
#             resp.say("Aadhaar missing. Please start again.")
#             resp.redirect("/api/twilio/voice")
#             return make_response(str(resp), 200, {"Content-Type": "text/xml"})

#         mobile_e164 = AADHAR_MOBILE_MAP.get(aadhar)
#         if not mobile_e164:
#             resp.say(
#                 "This Aadhaar is not registered with Dev Dham Path. "
#                 "Please use the app or website to register first. Jai Somnath."
#             )
#             resp.hangup()
#             return make_response(str(resp), 200, {"Content-Type": "text/xml"})

#         # Extract plain 10 digit mobile (assuming +91XXXXXXXXXX)
#         plain_mobile = mobile_e164[-10:]

#         # Check if user already exists with that mobile
#         user = User.query.filter_by(mobile_no=plain_mobile).first()
#         if not user:
#             resp.say(
#                 "Your mobile number is not registered in Dev Dham Path system. "
#                 "Please complete registration from app or website. Jai Somnath."
#             )
#             resp.hangup()
#             return make_response(str(resp), 200, {"Content-Type": "text/xml"})

#         # Decide darshan date
#         today = datetime.now().date()
#         if choice == "1":
#             darshan_date = today
#         elif choice == "2":
#             darshan_date = today + timedelta(days=1)
#         else:
#             resp.say("Invalid choice. Please try again.")
#             resp.redirect(f"/api/twilio/darshan-date?aadhar={aadhar}")
#             return make_response(str(resp), 200, {"Content-Type": "text/xml"})

#         # Find first available Darshan slot
#         slot = find_first_available_slot("Darshan", darshan_date)
#         if not slot:
#             resp.say(
#                 "Sorry, there are no available darshan slots for the selected date. "
#                 "Please try another day. Jai Somnath."
#             )
#             resp.hangup()
#             return make_response(str(resp), 200, {"Content-Type": "text/xml"})

#         # Create a minimal passenger using Aadhaar as ID
#         passenger = Passenger(
#             user_id=user.id,
#             slot_id=slot.id,
#             darshan_date=darshan_date,
#             name=user.name or "Devotee",
#             special=False,
#             with_special=False,
#             aadhaar_number=aadhar,
#             age=0,
#             gender="",
#             priority=0,
#             wheelchairneeded=False
#         )
#         db.session.add(passenger)
#         db.session.flush()  # to get passenger.id

#         # Generate QR and store
#         qr_payload = str({
#             "name": passenger.name,
#             "passenger_id": passenger.id,
#             "darshan_date": darshan_date.isoformat(),
#             "slot_id": slot.id,
#             "aadhar": aadhar,
#             "special": False,
#             "with_special": False,
#             "priority": 0
#         })
#         qr_filename = f"ivr_passenger_{passenger.id}.png"
#         encoded = qrgenerator(qr_payload, qr_filename)
#         passenger.qr_code = encoded

#         db.session.commit()

#         # Send WhatsApp ticket to mapped mobile
#         try:
#             slot_type = slot.slot_type
#             slot_text = f"{slot.start_time.strftime('%H:%M')} to {slot.end_time.strftime('%H:%M')}"
#             TWILIO_CLIENT.messages.create(
#                 from_=TWILIO_WHATSAPP_NUMBER,
#                 body=(
#                     f"{slot_type} Ticket #{passenger.id} booked for {passenger.name}.\n"
#                     f"Date: {darshan_date.isoformat()}\n"
#                     f"Slot: {slot_text}\n"
#                     f"Jai Somnath - DevDhamPath"
#                 ),
#                 media_url=[f"{clouflare_url}/api/qrcode/{qr_filename}"],
#                 to=f"whatsapp:{mobile_e164}"
#             )
#         except Exception as e:
#             print("WhatsApp Error in IVR Darshan booking:", e)

#         # Voice confirmation
#         resp.say(
#             f"Your Sugam Darshan ticket has been booked successfully. "
#             f"Ticket I D {passenger.id}. "
#             "A WhatsApp confirmation with QR code has been sent to your registered mobile number. "
#             "Jai Somnath."
#         )
#         resp.hangup()

#         return make_response(str(resp), 200, {"Content-Type": "text/xml"})
    
# api.add_resource(TwilioIVRStart, "/twilio/voice")
# api.add_resource(TwilioIVRMenu, "/twilio/menu")
# api.add_resource(TwilioIVRAadhaarDarshan, "/twilio/aadhar-darshan")
# api.add_resource(TwilioIVRAadhaarDarshanVerify, "/twilio/aadhar-darshan-verify")
# api.add_resource(TwilioIVRDarshanDate, "/twilio/darshan-date")

class TwilioIVRStart(Resource):
    """
    Entry point for IVR. First: choose language.
    /api/twilio/voice
    """
    def post(self):
        resp = VoiceResponse()

        gather = resp.gather(
            num_digits=1,
            action="/api/twilio/lang-select",
            method="POST"
        )
        # Default language while choosing? Use en-IN but Hindi sentence bhi chalega.
        gather.say(t("en", "lang_select"), **LANG_VOICE["en"])

        resp.say(t("en", "no_input"), **LANG_VOICE["en"])
        resp.say(t("en", "goodbye"), **LANG_VOICE["en"])

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

    
class TwilioIVRMenu(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        digits = request.values.get("Digits")

        if digits is None:
            # First time arriving here from lang-select: speak menu
            gather = resp.gather(
                num_digits=1,
                action=f"/api/twilio/menu?lang={lang}",
                method="POST"
            )
            gather.say(t(lang, "main_menu"), **LANG_VOICE[lang])

            resp.say(t(lang, "no_input"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/menu?lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # User has pressed a key
        if digits == "1":
            resp.redirect(f"/api/twilio/aadhar-darshan?lang={lang}")
        elif digits == "2":
            msg = (
                "Aarti booking via phone will be available soon. Please use the app. Jai Somnath."
                if lang == "en"
                else "Phone se Aarti booking jaldi hi uplabdh hogi. Kripya app ka upyog karein. Jai Somnath."
            )
            resp.say(msg, **LANG_VOICE[lang])
            resp.say(t(lang, "goodbye"), **LANG_VOICE[lang])
            resp.hangup()
        else:
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/menu?lang={lang}")

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})


class TwilioIVRAadhaarDarshan(Resource):
    """
    Step 1: Ask devotee to enter 12-digit Aadhaar.
    """
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        gather = resp.gather(
            num_digits=12,
            action=f"/api/twilio/aadhar-darshan-verify?lang={lang}",
            method="POST"
        )
        gather.say(t(lang, "aadhaar_prompt"), **LANG_VOICE[lang])

        resp.say(t(lang, "no_input"), **LANG_VOICE[lang])
        resp.redirect(f"/api/twilio/aadhar-darshan?lang={lang}")
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})
    
class TwilioIVRAadhaarDarshanVerify(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        aadhar = request.values.get("Digits")

        if not aadhar:
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/aadhar-darshan?lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        mobile_e164 = AADHAR_MOBILE_MAP.get(aadhar)
        if not mobile_e164:
            resp.say(t(lang, "aadhaar_not_registered"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        plain_mobile = mobile_e164[-10:]
        user = User.query.filter_by(mobile_no=plain_mobile).first()
        if not user:
            resp.say(t(lang, "mobile_not_registered"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        gather = resp.gather(
            num_digits=1,
            action=f"/api/twilio/darshan-date-ask?aadhar={aadhar}&lang={lang}",
            method="POST"
        )
        gather.say(t(lang, "day_prompt"), **LANG_VOICE[lang])

        resp.say(t(lang, "no_input"), **LANG_VOICE[lang])
        resp.redirect(f"/api/twilio/darshan-date-ask?aadhar={aadhar}&lang={lang}")
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})


class TwilioIVRDarshanDateAsk(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        aadhar = request.args.get("aadhar")
        choice = request.values.get("Digits")

        if not aadhar or not choice:
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/voice")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        try:
            choice_int = int(choice)
        except ValueError:
            choice_int = 0

        if choice_int < 1 or choice_int > 7:
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/darshan-date-ask?aadhar={aadhar}&lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        today = datetime.now().date()
        darshan_date = today + timedelta(days=choice_int - 1)
        date_str = darshan_date.isoformat()

        resp.redirect(f"/api/twilio/darshan-slot-ask?aadhar={aadhar}&date={date_str}&lang={lang}")
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})


class TwilioIVRDarshanSlotAsk(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")

        if not aadhar or not date_str:
            resp.say(t(lang, "internal_error"), **LANG_VOICE[lang])
            resp.redirect("/api/twilio/voice")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        try:
            _ = datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            resp.say(t(lang, "internal_error"), **LANG_VOICE[lang])
            resp.redirect("/api/twilio/voice")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        slots = get_ordered_darshan_slots()
        if not slots:
            resp.say(t(lang, "darshan_not_configured"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        speak_lines = []
        option = 1
        for s in slots:
            start_txt = s.start_time.strftime("%I:%M %p")
            end_txt = s.end_time.strftime("%I:%M %p")
            if lang == "en":
                speak_lines.append(f"For {start_txt} to {end_txt}, press {option}.")
            else:
                speak_lines.append(
                    f"{start_txt} se {end_txt} ke darshan ke liye, {option} dabaiye."
                )
            option += 1

        gather = resp.gather(
            num_digits=1,
            action=f"/api/twilio/darshan-slot-select?aadhar={aadhar}&date={date_str}&lang={lang}",
            method="POST"
        )
        gather.say(
            t(lang, "slot_intro") + " " + " ".join(speak_lines),
            **LANG_VOICE[lang]
        )

        resp.say(t(lang, "no_input"), **LANG_VOICE[lang])
        resp.redirect(f"/api/twilio/darshan-slot-ask?aadhar={aadhar}&date={date_str}&lang={lang}")
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

class TwilioIVRDarshanConfirm(Resource):
    """
    Step 8: Receive wheelchair choice, then:
    - capacity check
    - compute special & priority
    - create Passenger
    - generate QR
    - send WhatsApp
    - voice confirmation
    """
    def post(self):
        resp = VoiceResponse()
        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")
        gender_str = request.args.get("gender")
        age_str = request.args.get("age")
        wc_digit = request.values.get("Digits")

        if not all([aadhar, date_str, slot_id, gender_str, age_str, wc_digit]):
            resp.say("Missing data. Please start again.")
            resp.redirect("/api/twilio/voice")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # wheelchair flag
        if wc_digit == "1":
            wheelchair_needed = True
        elif wc_digit == "2":
            wheelchair_needed = False
        else:
            resp.say("Invalid option. Please try again.")
            resp.redirect(
                f"/api/twilio/darshan-wheelchair?"
                f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
                f"&gender={gender_str}"
            )
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # parse age & date
        try:
            age_int = int(age_str)
            darshan_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            slot_id_int = int(slot_id)
        except Exception:
            resp.say("Internal error in data. Please try again later.")
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # Aadhaar -> mobile -> user
        mobile_e164 = AADHAR_MOBILE_MAP.get(aadhar)
        if not mobile_e164:
            resp.say("Aadhaar not registered with DevDhamPath. Jai Somnath.")
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        plain_mobile = mobile_e164[-10:]
        user = User.query.filter_by(mobile_no=plain_mobile).first()
        if not user:
            resp.say("Mobile not registered as user. Please use app to register. Jai Somnath.")
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        slot = Aarti_and_DarshanSlot.query.get(slot_id_int)
        if not slot:
            resp.say("Selected slot is not available. Please try again.")
            resp.redirect(f"/api/twilio/darshan-slot-ask?aadhar={aadhar}&date={date_str}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # Capacity check
        booked_count = Passenger.query.filter_by(
            slot_id=slot.id,
            darshan_date=darshan_date
        ).count()
        if booked_count >= slot.max_visitors:
            resp.say(
                "Sorry, this slot is already full. "
                "Please select a different slot."
            )
            resp.redirect(f"/api/twilio/darshan-slot-ask?aadhar={aadhar}&date={date_str}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # Compute special + priority like tumhaara normal logic
        is_special = False
        priority = 0

        if age_int >= 60:
            is_special = True
            if 60 <= age_int < 70:
                priority += 1
            else:  # 70+
                priority += 2

        if wheelchair_needed:
            is_special = True
            priority += 4

        # Create Passenger
        passenger = Passenger(
            user_id=user.id,
            slot_id=slot.id,
            darshan_date=darshan_date,
            name=user.name or "Devotee",
            aadhaar_number=aadhar,
            qr_code=None,
            scan_count=0,
            special=is_special,
            with_special=False,
            age=age_int,
            gender=gender_str,
            priority=priority,
            wheelchairneeded=wheelchair_needed
        )
        db.session.add(passenger)
        db.session.flush()  # get ID

        # QR payload
        qr_payload = str({
            "name": passenger.name,
            "passenger_id": passenger.id,
            "darshan_date": darshan_date.isoformat(),
            "slot_id": slot.id,
            "aadhar": aadhar,
            "special": is_special,
            "with_special": False,
            "priority": priority,
            "age": age_int,
            "gender": gender_str,
            "wheelchairneeded": wheelchair_needed
        })
        qr_filename = f"ivr_passenger_{passenger.id}.png"
        encoded = qrgenerator(qr_payload, qr_filename)
        passenger.qr_code = encoded

        db.session.commit()

        # WhatsApp ticket
        try:
            slot_text = f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
            TWILIO_CLIENT.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=(
                    f"Sugam Darshan Ticket #{passenger.id}\n"
                    f"Name: {passenger.name}\n"
                    f"Date: {darshan_date.isoformat()}\n"
                    f"Slot: {slot_text}\n"
                    f"Age: {age_int}, Gender: {gender_str}\n"
                    f"Wheelchair: {'Yes' if wheelchair_needed else 'No'}\n"
                    f"Jai Somnath - DevDhamPath"
                ),
                media_url=[f"{clouflare_url}/api/qrcode/{qr_filename}"],
                to=f"whatsapp:{mobile_e164}"
            )
        except Exception as e:
            print("WhatsApp Error in IVR booking:", e)

        resp.say(
            f"Your Sugam Darshan ticket has been booked successfully. "
            f"Ticket I D {passenger.id}. "
            "A WhatsApp confirmation with Q R code has been sent to your registered mobile number. "
            "Jai Somnath."
        )
        resp.hangup()
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})


class TwilioIVRDarshanSlotSelect(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        choice = request.values.get("Digits")

        if not aadhar or not date_str or not choice:
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/darshan-slot-ask?aadhar={aadhar}&date={date_str}&lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        slots = get_ordered_darshan_slots()
        if not slots:
            resp.say(t(lang, "darshan_not_configured"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        try:
            idx = int(choice) - 1
        except ValueError:
            idx = -1

        if idx < 0 or idx >= len(slots):
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/darshan-slot-ask?aadhar={aadhar}&date={date_str}&lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        slot = slots[idx]
        resp.redirect(
            f"/api/twilio/darshan-gender?aadhar={aadhar}&date={date_str}&slot_id={slot.id}&lang={lang}"
        )
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})
        
class TwilioIVRDarshanGender(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")

        if not aadhar or not date_str or not slot_id:
            resp.say(t(lang, "internal_error"), **LANG_VOICE[lang])
            resp.redirect("/api/twilio/voice")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        gather = resp.gather(
            num_digits=1,
            action=f"/api/twilio/darshan-age?aadhar={aadhar}&date={date_str}&slot_id={slot_id}&lang={lang}",
            method="POST"
        )
        gather.say(t(lang, "gender_prompt"), **LANG_VOICE[lang])

        resp.say(t(lang, "no_input"), **LANG_VOICE[lang])
        resp.redirect(f"/api/twilio/darshan-gender?aadhar={aadhar}&date={date_str}&slot_id={slot_id}&lang={lang}")
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})


class TwilioIVRDarshanAge(Resource):
    """
    Step 6: Receive gender digit, then ask for age (2 digits).
    """
    def post(self):
        resp = VoiceResponse()
        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")
        gender_digit = request.values.get("Digits")

        if not aadhar or not date_str or not slot_id or not gender_digit:
            resp.say("Invalid input. Please try again.")
            resp.redirect("/api/twilio/voice")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        if gender_digit == "1":
            gender_str = "Male"
        elif gender_digit == "2":
            gender_str = "Female"
        elif gender_digit == "3":
            gender_str = "Other"
        else:
            resp.say("Invalid gender option. Please try again.")
            resp.redirect(f"/api/twilio/darshan-gender?aadhar={aadhar}&date={date_str}&slot_id={slot_id}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # Ask for age
        gather = resp.gather(
            num_digits=2,
            action=(
                f"/api/twilio/darshan-wheelchair?"
                f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}&gender={gender_str}"
            ),
            method="POST"
        )
        gather.say(
            "Please enter age in years using two digits. "
            "For example, for twenty five, press 2 and 5."
        )

        resp.say("No input received. Restarting.")
        resp.redirect(
            f"/api/twilio/darshan-age?aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
        )
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})
    
class TwilioIVRDarshanWheelchair(Resource):
    """
    Step 7: Receive age, then ask if wheelchair is needed.
    """
    def post(self):
        resp = VoiceResponse()
        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")
        gender_str = request.args.get("gender")
        age_digits = request.values.get("Digits")

        if not aadhar or not date_str or not slot_id or not gender_str or not age_digits:
            resp.say("Invalid input. Please start again.")
            resp.redirect("/api/twilio/voice")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        try:
            age_int = int(age_digits)
        except ValueError:
            resp.say("Invalid age. Please enter a valid age.")
            resp.redirect(
                f"/api/twilio/darshan-age?aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
            )
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        if age_int <= 0 or age_int > 120:
            resp.say("Invalid age. Please enter a valid age.")
            resp.redirect(
                f"/api/twilio/darshan-age?aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
            )
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # Ask if wheelchair is needed
        gather = resp.gather(
            num_digits=1,
            action=(
                f"/api/twilio/darshan-confirm?"
                f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
                f"&gender={gender_str}&age={age_int}"
            ),
            method="POST"
        )
        gather.say(
            "If wheelchair assistance is needed, press 1. "
            "If wheelchair is not needed, press 2."
        )

        resp.say("No input received. Restarting.")
        resp.redirect(
            f"/api/twilio/darshan-wheelchair?aadhar={aadhar}&date={date_str}"
            f"&slot_id={slot_id}&gender={gender_str}"
        )
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})
    
PROMPTS = {
    "en": {
        "lang_select": (
            "Welcome to Dev Dham Path. "
            "For Hindi, press 1. "
            "For English, press 2."
        ),
        "main_menu": (
            "Jai Somnath. "
            "For Sugam Darshan ticket booking, press 1. "
            "For Sugam Aarti booking, press 2."
        ),
        "invalid_choice": "Invalid choice.",
        "no_input": "No input received. Restarting.",
        "goodbye": "Jai Somnath. Goodbye.",
        "aadhaar_prompt": (
            "Please enter your twelve digit Aadhaar number, "
            "followed by the hash key."
        ),
        "aadhaar_not_registered": (
            "This Aadhaar is not registered with Dev Dham Path. "
            "Please register from the app or website. Jai Somnath."
        ),
        "mobile_not_registered": (
            "Your mobile number is not registered as a user. "
            "Please complete registration from the app. Jai Somnath."
        ),
        "day_prompt": (
            "Please choose your darshan day. "
            "For today, press 1. "
            "For tomorrow, press 2. "
            "For day after tomorrow, press 3. "
            "For fourth day from today, press 4. "
            "For fifth day, press 5. "
            "For sixth day, press 6. "
            "For seventh day, press 7."
        ),
        "slot_intro": "Please choose your Sugam Darshan time slot.",
        "gender_prompt": (
            "Please select gender. "
            "For male, press 1. "
            "For female, press 2. "
            "For other, press 3."
        ),
        "age_prompt": (
            "Please enter age in years using two digits. "
            "For example, for twenty five, press 2 and 5."
        ),
        "wheelchair_prompt": (
            "If wheelchair assistance is needed, press 1. "
            "If wheelchair is not needed, press 2."
        ),
        "slot_full": (
            "Sorry, this slot is already full. "
            "Please select a different slot."
        ),
        "internal_error": "Internal error. Please try again later.",
        "darshan_not_configured": (
            "Darshan timings are not configured. Please try later. Jai Somnath."
        ),
        "booking_confirm": (
            "Your Sugam Darshan ticket has been booked successfully. "
            "A WhatsApp confirmation with QR code has been sent to your registered mobile number. "
            "Jai Somnath."
        ),
    },
    "hi": {
        "lang_select": (
            "Dev Dham Path mein aapka swagat hai. "
            "Hindi ke liye 1 dabaiye. "
            "Angrezi ke liye 2 dabaiye."
        ),
        "main_menu": (
            "Jai Somnath. "
            "Sugam Darshan ticket booking ke liye 1 dabaiye. "
            "Sugam Aarti booking ke liye 2 dabaiye."
        ),
        "invalid_choice": "Galat vikalp hai.",
        "no_input": "Koi input nahi mila. Phir se koshish karte hain.",
        "goodbye": "Jai Somnath. Dhanyavaad.",
        "aadhaar_prompt": (
            "Kripya apna baarah ank ka Aadhar number darj karein "
            "aur hash key dabayein."
        ),
        "aadhaar_not_registered": (
            "Yeh Aadhar Dev Dham Path par registered nahi hai. "
            "Kripya app ya website se registration karein. Jai Somnath."
        ),
        "mobile_not_registered": (
            "Aapka mobile number system mein registered nahi hai. "
            "Kripya app se registration poora karein. Jai Somnath."
        ),
        "day_prompt": (
            "Kripya apni darshan ki tithi chunen. "
            "Aaj ke liye 1 dabaiye. "
            "Kal ke liye 2. "
            "Parson ke liye 3. "
            "Chauthe din ke liye 4. "
            "Paanchve din ke liye 5. "
            "Chhathe din ke liye 6. "
            "Saathve din ke liye 7 dabaiye."
        ),
        "slot_intro": "Kripya apna Sugam Darshan time slot chunen.",
        "gender_prompt": (
            "Kripya ling chunen. "
            "Purush ke liye 1 dabaiye. "
            "Mahila ke liye 2. "
            "Any ke liye 3."
        ),
        "age_prompt": (
            "Kripya apni umra do ank mein darj karein. "
            "Jaise pachis ke liye 2 aur 5 dabaiye."
        ),
        "wheelchair_prompt": (
            "Yadi wheelchair sahayata chahiye to 1 dabaiye. "
            "Yadi wheelchair nahi chahiye to 2 dabaiye."
        ),
        "slot_full": (
            "Maaf kijiye, yeh slot poori tarah bhara hua hai. "
            "Kripya koi doosra slot chunen."
        ),
        "internal_error": "System mein kuch dikkat hai. Kripya baad mein koshish karein.",
        "darshan_not_configured": (
            "Darshan ke samay set nahi kiye gaye hain. "
            "Kripya baad mein koshish karein. Jai Somnath."
        ),
        "booking_confirm": (
            "Aapka Sugam Darshan ticket safal roop se buk ho gaya hai. "
            "QR code ke saath WhatsApp par pushti sandesh bhej diya gaya hai. "
            "Jai Somnath."
        ),
    },
}

LANG_VOICE = {
    "en": {"language": "en-IN"},
    "hi": {"language": "hi-IN"},
}

def get_lang():
    lang = request.args.get("lang", "en")
    return "hi" if lang == "hi" else "en"

def t(lang, key):
    return PROMPTS.get(lang, PROMPTS["en"]).get(key, PROMPTS["en"].get(key, ""))    

class TwilioIVRLanguageSelect(Resource):
    """
    Map digit → lang code, then go to main menu with ?lang=...
    """
    def post(self):
        resp = VoiceResponse()
        choice = request.values.get("Digits")

        if choice == "1":
            lang = "hi"
        elif choice == "2":
            lang = "en"
        else:
            # default English
            lang = "en"
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])

        resp.redirect(f"/api/twilio/menu?lang={lang}")
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

    
api.add_resource(TwilioIVRStart, "/twilio/voice")
api.add_resource(TwilioIVRLanguageSelect, "/twilio/lang-select")
api.add_resource(TwilioIVRMenu, "/twilio/menu")
api.add_resource(TwilioIVRAadhaarDarshan, "/twilio/aadhar-darshan")
api.add_resource(TwilioIVRAadhaarDarshanVerify, "/twilio/aadhar-darshan-verify")
api.add_resource(TwilioIVRDarshanDateAsk, "/twilio/darshan-date-ask")
api.add_resource(TwilioIVRDarshanSlotAsk, "/twilio/darshan-slot-ask")
api.add_resource(TwilioIVRDarshanSlotSelect, "/twilio/darshan-slot-select")
api.add_resource(TwilioIVRDarshanGender, "/twilio/darshan-gender")
api.add_resource(TwilioIVRDarshanAge, "/twilio/darshan-age")
api.add_resource(TwilioIVRDarshanWheelchair, "/twilio/darshan-wheelchair")
api.add_resource(TwilioIVRDarshanConfirm, "/twilio/darshan-confirm")

# Initialize properly (two args)
if SMS_SID and SMS_TOKEN:
    SMS_CLIENT = Client(SMS_SID, SMS_TOKEN)
else:
    SMS_CLIENT = None
    print("[SMS INIT] WARNING: SMS client not initialized. Check SMS_SID/SMS_TOKEN.")

def send_sms(to_number: str, body: str):
    """
    Send a plain SMS using SMS_CLIENT.
    - Expects 'to_number' and SMS_NUMBER to be in E.164 format (eg '+919876543210').
    - If you use a Messaging Service SID, pass it via messaging_service_sid instead of from_.
    """
    global SMS_CLIENT, SMS_NUMBER

    if not SMS_CLIENT:
        print("[SMS ERROR] SMS_CLIENT not initialized (missing SID/TOKEN)")
        return

    if not SMS_NUMBER:
        print("[SMS ERROR] SMS_NUMBER not configured")
        return

    # Ensure to_number is E.164. If it's missing '+' and country code, try to fix for India:
    if not to_number.startswith("+"):
        # optional: automatically prepend +91 if numeric and len ==10
        if to_number.isdigit() and len(to_number) == 10:
            to_number = "+91" + to_number
            print("[SMS] Normalized recipient to", to_number)
        else:
            print("[SMS ERROR] to_number not in E.164 and not fixable:", to_number)
            return

    try:
        msg = SMS_CLIENT.messages.create(
            from_=SMS_NUMBER,   # must be Twilio number in E.164 or use messaging_service_sid=
            to=to_number,
            body=body
        )
        print("[SMS SENT]", to_number, "sid=", getattr(msg, "sid", None))
    except Exception as e:
        # Log full exception for debug
        print("[SMS ERROR] Failed sending to", to_number, ":", repr(e))


def notify_gate_closed():
    """
    Called when gate goes from OPEN -> CLOSED.
    """
    security_msg = (
        "ALERT: Entry gate CLOSED. Mandir crowd at maximum capacity. "
        "Please manage the hall and control queues."
    )
    bus_msg = (
        "ALERT: Entry gate CLOSED. Please temporarily stop shuttle buses "
        "from bringing more devotees until further notice."
    )

    send_sms(SECURITY_OFFICER, security_msg)
    send_sms(SHUTTLE_BUS, bus_msg)


def notify_gate_opened():
    """
    Called when gate goes from CLOSED -> OPEN.
    """
    security_msg = (
        "UPDATE: Mandir crowd is now under control. Entry gate OPEN. "
        "Resume normal crowd flow."
    )
    bus_msg = (
        "UPDATE: Entry gate OPEN. You can resume normal shuttle bus operations."
    )

    send_sms(SECURITY_OFFICER, security_msg)
    send_sms(SHUTTLE_BUS, bus_msg)

def update_gate_state_and_notify():
    """
    Recalculate gate state (FLAG) from CURRENT_COUNT_MANDIR
    and send SMS when it flips OPEN <-> CLOSED.

    FLAG: 0 = OPEN, 1 = CLOSED
    """
    global CURRENT_COUNT_MANDIR, MAX_COUNT_MANDIR, MIN_COUNT_MADIR, FLAG

    previous_flag = FLAG

    # Recalculate based on current crowd count
    if CURRENT_COUNT_MANDIR >= MAX_COUNT_MANDIR:
        FLAG = 1    # gate closed
    elif CURRENT_COUNT_MANDIR <= MIN_COUNT_MADIR:
        FLAG = 0    # gate open

    # If state changed, send appropriate SMS
    if previous_flag == 0 and FLAG == 1:
        print("[GATE STATE] OPEN -> CLOSED")
        notify_gate_closed()

    elif previous_flag == 1 and FLAG == 0:
        print("[GATE STATE] CLOSED -> OPEN")
        notify_gate_opened()