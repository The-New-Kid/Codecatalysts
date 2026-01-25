from asyncio import gather
from twilio.twiml.voice_response import VoiceResponse, Gather

# routes_emergency.py
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from collections import deque
import uuid
from math import radians, sin, cos, sqrt, atan2

from blockchain.registry import issue_hash
import ast
from flask import request,current_app as app,make_response,send_from_directory
from flask_restful import Api,Resource,fields, marshal_with,marshal
from models.model import *
import mimetypes
import os
import requests
import calendar
#from pyzbar.pyzbar import decode
from crowd_model import predict_crowd_for_date
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
import hashlib
import cv2
from werkzeug.security import generate_password_hash, check_password_hash
from gittest import super
load_dotenv()
CURRENT_COUNT_MANDIR=0
MAX_COUNT_MANDIR=3
MIN_COUNT_MADIR=1
FLAG=0
api=Api(prefix='/api')
otp_login_storage = {}
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
CONTENT_SID = os.getenv("CONTENT_SID")
clouflare_url=os.getenv("PUBLIC_BASE_URL")
TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

VANSH_TWILIO_SID=os.getenv("VANSH_TWILIO_SID")
VANSH_TWILIO_AUTH=os.getenv("VANSH_TWILIO_AUTH")
TWILIO_SMS_NUMBER=os.getenv("TWILIO_SMS_NUMBER")

TWILIO_SMS_CLIENT=Client(VANSH_TWILIO_SID,VANSH_TWILIO_AUTH)
POLICE_NUMBER="+916389890800"

IVR_TWILIO_SID = os.getenv("IVR_TWILIO_SID")
IVR_AUTH_TOKEN = os.getenv("IVR_AUTH_TOKEN")
IVR_NUMBER = os.getenv("IVR_NUMBER")

IVR_CLIENT = Client(IVR_TWILIO_SID, IVR_AUTH_TOKEN, IVR_NUMBER)
SHUTTLE_BUS_VAALA="+916396526619"
SECURITY_OFFICER_NUMBER="+917456097831"

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
        base_path = os.path.abspath(os.path.join(app.root_path, '..','backend', 'static', 'qrcode'))
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

        # 🔹 Map numeric role -> string role
        if user.role == 0:
            role = "admin"
        elif user.role == 2:
            role = "securityguard"   # 👈 NEW
        else:
            role = "user"

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
        type=data.get("type")
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

        print(selected_date)
        max_visitor_multiplier=None
        if type=="aarti" or type=="darshan":
            max_visitor_multiplier=0.75
        elif type=="aarti_tatkal" or type=="darshan_tatkal":
            max_visitor_multiplier=0.2
        else:
            pass
        crowd=PanchangCache.query.filter_by(day=selected_date.day,month=selected_date.month,year=selected_date.year).first()
        print(crowd.crowd)
        print(max_visitor_multiplier)
        if(crowd.crowd<15000):
            max_visitor_multiplier=max_visitor_multiplier*0.8
        elif(crowd.crowd>=15000 and crowd.crowd<25000):
            max_visitor_multiplier=max_visitor_multiplier*0.9
        else:
            pass
        num_members = len(passengers)

        already_booked = Passenger.query.filter_by(
            slot_id=slot_id,
            darshan_date=selected_date
        ).count()

        if already_booked + num_members > int(slot.max_visitors*max_visitor_multiplier):
            return {
                "success": False,
                "message": f"Only {int(slot.max_visitors*max_visitor_multiplier) - already_booked} slots left"
            }, 400

        # QR Setup
        QR_FOLDER = os.path.join("static", "qrcode")
        os.makedirs(QR_FOLDER, exist_ok=True)

        booked_passengers = []

        # Saving all passengers with updated priority logic
        for idx, p in enumerate(passengers):
            name = p.get("name")
            aadhar = p.get("aadhar")
            otp_entered = p.get("otp")

            # OTP Check
            if otp_storage.get(aadhar) != otp_entered:
                return {"success": False, "message": f"OTP failed for {name}"}, 402

            otp_storage.pop(aadhar, None)

            age = int(p.get("age", 0))
            wheelchair_needed = p.get("wheelchair_needed", False)
            gender = p.get("gender", "")

            # NEW PRIORITY CALCULATION
            if age >= 70:
                priority = 3
            elif age >= 60:
                priority = 2
            else:
                priority = 0

            if wheelchair_needed:
                priority += 4

            passenger = Passenger(
                user_id=user.id,
                slot_id=slot.id,
                darshan_date=selected_date,
                name=name,
                aadhaar_number=aadhar,
                age=age,
                gender=gender,
                priority=priority,
                wheelchairneeded=wheelchair_needed
            )
            db.session.add(passenger)
            db.session.flush()

            # Generate QR
            metadata = {
                    "name": name,
                    "passenger_id": passenger.id,
                    "darshan_date": str(darshan_date),
                    "slot_id": slot_id,
                    "aadhar": aadhar,
                    "priority": priority
                }
            metadata_json = json.dumps(metadata, sort_keys=True, separators=(",", ":"))
            hash_hex = hashlib.sha256(metadata_json.encode()).hexdigest()
            issue_hash(hash_hex)
            qr_payload = {
                "metadata": metadata,
                "hash": hash_hex
            }
            qr_data = json.dumps(qr_payload, separators=(",", ":"))
            qr_filename = f"passenger_{passenger.id}_{secure_filename(name)}.png"
            encoded = qrgenerator(qr_data, qr_filename)
            passenger.qr_code = encoded

            # WhatsApp Sending
            slot_type = passenger.slot.slot_type
            try:
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=f"{slot_type} Ticket #{passenger.id} booked for {name}",
                    to=f"whatsapp:+91{mobile_number}"
                )
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


def get_ordered_darshan_slots():
    """
    Return all Darshan slots ordered by start_time.
    Used by IVR slot selection.
    """
    return Aarti_and_DarshanSlot.query.filter_by(
        slot_type="Darshan"
    ).order_by(Aarti_and_DarshanSlot.start_time).all()



api.add_resource(BookTicketResource, '/book-ticket')
# -------------------------------------------
API_USER = os.getenv("CALANDER_UID")
API_KEY = os.getenv("CALANDER_API_KEY")

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
        ticket = None

        file = request.files.get('qr_image')
        if not file or file.filename == '':
            return {
                "success": False,
                "message": "❌ No image uploaded."
            }, 400

        try:
            # Save image
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            img = cv2.imread(filepath)
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(img)

            if not data:
                return {
                    "success": False,
                    "message": "❌ Could not read QR code."
                }, 400

            # Handle base64 or plain text
            try:
                decoded = Base64.b64decode(data).decode("utf-8")
            except Exception:
                decoded = data

            # ---------------- QR PARSING ---------------- #
            try:
                qr_payload = json.loads(decoded)
                metadata = qr_payload.get("metadata")
                hash_from_qr = qr_payload.get("hash")

                if not metadata or not hash_from_qr:
                    return {
                        "success": False,
                        "message": "❌ Invalid QR format."
                    }, 400

                passenger_id = metadata.get("passenger_id")
                if not passenger_id:
                    return {
                        "success": False,
                        "message": "❌ Passenger ID missing."
                    }, 400

            except Exception:
                return {
                    "success": False,
                    "message": "❌ Invalid QR code content."
                }, 400

            # ---------------- HASH INTEGRITY CHECK ---------------- #
            metadata_json = json.dumps(
                metadata,
                sort_keys=True,
                separators=(",", ":")
            )
            recomputed_hash = hashlib.sha256(
                metadata_json.encode()
            ).hexdigest()

            if recomputed_hash != hash_from_qr:
                return {
                    "success": False,
                    "message": "❌ QR data has been tampered."
                }, 403

            # ---------------- BLOCKCHAIN VERIFICATION ---------------- #
            from blockchain.registry import verify_hash

            if not verify_hash(hash_from_qr):
                return {
                    "success": False,
                    "message": "❌ Ticket invalid or revoked (blockchain)."
                }, 403

            # ---------------- EXISTING DB + GATE LOGIC ---------------- #
            ticket = Passenger.query.get(passenger_id)
            if not ticket:
                return {
                    "success": False,
                    "message": "❌ Ticket not found."
                }, 404

            global CURRENT_COUNT_MANDIR
            global MAX_COUNT_MANDIR
            global MIN_COUNT_MADIR
            global FLAG

            if MAX_COUNT_MANDIR == CURRENT_COUNT_MANDIR:
                FLAG = 1
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body="STOP BUS SERVICE.",
                    to=f"whatsapp:{SHUTTLE_BUS_VAALA}"
                )
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body="CLOSE GATES",
                    to=f"whatsapp:{SECURITY_OFFICER_NUMBER}"
                )

            if MIN_COUNT_MADIR == CURRENT_COUNT_MANDIR:
                FLAG = 0
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body="START BUS SERVICE.",
                    to=f"whatsapp:{SHUTTLE_BUS_VAALA}"
                )
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body="GATES OPENING",
                    to=f"whatsapp:{SECURITY_OFFICER_NUMBER}"
                )

            if ticket.scan_count == 0 and FLAG == 0:
                ticket.scan_count = 1
                CURRENT_COUNT_MANDIR += 1
                message = f"✅ Entry granted for Ticket {ticket.id}"

            elif ticket.scan_count == 1:
                ticket.scan_count = 2
                CURRENT_COUNT_MANDIR -= 1
                message = f"✅ Exit recorded for Ticket {ticket.id}"

            elif ticket.scan_count == 2:
                message = f"❌ Ticket {ticket.id} already expired."

            else:
                message = "❌ Mandir is currently full, please wait."

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
            return {
                "success": False,
                "message": f"❌ Error processing image: {e}"
            }, 500


class ScanTicketLiveResource(Resource):

    def post(self):
        try:
            data = request.get_json(force=True, silent=True) or {}
            qr_text = data.get("qr_text")

            if not qr_text:
                return {"success": False, "message": "❌ No QR text provided."}, 400

            # -------- Normalize QR text -------- #
            try:
                if isinstance(qr_text, str):
                    qr_bytes = qr_text.encode("utf-8")
                else:
                    qr_bytes = qr_text

                try:
                    decoded = Base64.b64decode(qr_bytes).decode("utf-8")
                except Exception:
                    decoded = qr_text if isinstance(qr_text, str) else qr_text.decode("utf-8")

            except Exception as e:
                return {"success": False, "message": f"❌ Failed to normalize QR text"}, 400

            # -------- Parse JSON -------- #
            try:
                qr_payload = json.loads(decoded)
                metadata = qr_payload.get("metadata")
                hash_from_qr = qr_payload.get("hash")

                if not metadata or not hash_from_qr:
                    return {"success": False, "message": "❌ Invalid QR format."}, 400

                passenger_id = metadata.get("passenger_id")
                if not passenger_id:
                    return {"success": False, "message": "❌ Passenger ID missing."}, 400

            except Exception:
                return {"success": False, "message": "❌ Invalid QR payload."}, 400

            # -------- Integrity check (hash) -------- #
            metadata_json = json.dumps(
                metadata,
                sort_keys=True,
                separators=(",", ":")
            )
            recomputed_hash = hashlib.sha256(
                metadata_json.encode()
            ).hexdigest()

            if recomputed_hash != hash_from_qr:
                return {
                    "success": False,
                    "message": "❌ QR data has been tampered."
                }, 403

            # -------- Blockchain verification -------- #
            from blockchain.registry import verify_hash

            if not verify_hash(hash_from_qr):
                return {
                    "success": False,
                    "message": "❌ Ticket invalid or revoked (blockchain)."
                }, 403

            # -------- Existing DB + gate logic -------- #
            ticket = Passenger.query.get(int(passenger_id))
            if not ticket:
                return {"success": False, "message": "❌ Ticket not found."}, 404

            global CURRENT_COUNT_MANDIR
            global MAX_COUNT_MANDIR
            global MIN_COUNT_MADIR
            global FLAG

            if MAX_COUNT_MANDIR == CURRENT_COUNT_MANDIR:
                FLAG = 1
            if MIN_COUNT_MADIR == CURRENT_COUNT_MANDIR:
                FLAG = 0

            if ticket.scan_count == 0 and FLAG == 0:
                ticket.scan_count = 1
                CURRENT_COUNT_MANDIR += 1
                message = f"✅ Entry granted for Ticket "

            elif ticket.scan_count == 1:
                ticket.scan_count = 2
                CURRENT_COUNT_MANDIR -= 1
                message = f"✅ Exit recorded for Ticket"

            elif ticket.scan_count == 2:
                message = f"❌ Ticket already expired."

            else:
                message = "❌ Mandir is currently full, please wait."

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
                    spot.status = 'O'
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
                    spot.status = 'O'
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
api.add_resource(SendOtpResource, '/send-otp')

class SubSlotAllocator(Resource):
    def post(self):
        today = datetime.now().date()

        slots = Aarti_and_DarshanSlot.query.all()
        chunk_minutes = 20

        for slot in slots:
            passengers = Passenger.query.filter_by(
                slot_id=slot.id,
                darshan_date=today
            ).order_by(Passenger.priority.desc(), Passenger.id).all()

            if not passengers:
                continue

            start_dt = datetime.combine(today, slot.start_time)
            end_dt = datetime.combine(today, slot.end_time)

            total_minutes = int((end_dt - start_dt).total_seconds() // 60)
            num_subslots = max(1, total_minutes // chunk_minutes)
            per_subslot = max(1, len(passengers) // num_subslots)

            idx = 0
            for subslot in range(num_subslots):
                sub_start = start_dt + timedelta(minutes=subslot * chunk_minutes)

                for _ in range(per_subslot):
                    if idx >= len(passengers):
                        break

                    passenger = passengers[idx]

                    # Notification time = 30min before subslot
                    notify_time = sub_start - timedelta(minutes=14)

                    # Send reminder
                    try:
                        user = User.query.get(passenger.user_id)
                        mobile = user.mobile_no
                        TWILIO_SMS_CLIENT.messages.create(
                            from_=TWILIO_SMS_NUMBER,
                            body=f"Reminder: Your Darshan sub-slot starts at "
                                 f"{sub_start.time().strftime('%H:%M')}. "
                                 "Please arrive 30 minutes early.",
                            to=f"+91{mobile}"
                        )
                        print(f"Notification sent to {passenger.name} for {sub_start.time()}")
                    except Exception as e:
                        print("WhatsApp Error:", e)

                    idx += 1

        return {"success": True, "message": "Sub-slots allocated & reminders sent"}
api.add_resource(SubSlotAllocator,"/allocate-subslots")




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
                "Aarti booking via phone will be available soon. Please use the app. Radhe Radhe."
                if lang == "en"
                else "Phone se Aarti booking jaldi hi uplabdh hogi. Kripya app ka upyog karein.Radhe Radhe."
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
            finishOnKey="#",
            timeout = 15,
            action=f"/api/twilio/aadhar-darshan-verify?lang={lang}",
            method="POST"
        )
        gather.say(t(lang, "aadhaar_prompt"), **LANG_VOICE[lang])

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})
    
class TwilioIVRAadhaarDarshanVerify(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        aadhar = (request.values.get("Digits") or "").strip()

        if not aadhar.isdigit() or len(aadhar) != 12:
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/aadhar-darshan?lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        mobile_e164 = AADHAR_MOBILE_MAP.get(aadhar)
        if not mobile_e164:
            resp.say(t(lang, "aadhaar_not_registered"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        gather = resp.gather(
            num_digits=1,
            finishOnKey="#",
            timeout=15,
            action=f"/api/twilio/darshan-date-handle?aadhar={aadhar}&lang={lang}",
            method="POST"
        )
        gather.say(t(lang, "day_prompt"), **LANG_VOICE[lang])

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

class TwilioIVRDarshanDateHandle(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        aadhar = request.args.get("aadhar")
        choice = (request.values.get("Digits") or "").strip()

        # THIS is where "galat vikalp" belongs
        if not choice.isdigit() or not (1 <= int(choice) <= 7):
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/darshan-date-ask?aadhar={aadhar}&lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        darshan_date = datetime.now().date() + timedelta(days=int(choice) - 1)

        resp.redirect(
            f"/api/twilio/darshan-slot-ask?"
            f"aadhar={aadhar}&date={darshan_date.isoformat()}&lang={lang}"
        )
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
            finishOnKey="#",
            timeout = 15,
            action=f"/api/twilio/aadhar-darshan-verify?lang={lang}",
            method="POST"
        )
        gather.say(t(lang, "aadhaar_prompt"), **LANG_VOICE[lang])

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})
    
class TwilioIVRAadhaarDarshanVerify(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        aadhar = (request.values.get("Digits") or "").strip()

        if not aadhar.isdigit() or len(aadhar) != 12:
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/aadhar-darshan?lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        mobile_e164 = AADHAR_MOBILE_MAP.get(aadhar)
        if not mobile_e164:
            resp.say(t(lang, "aadhaar_not_registered"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/aadhar-darshan?lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        plain_mobile = mobile_e164[-10:]
        user = User.query.filter_by(mobile_no=plain_mobile).first()
        if not user:
            resp.say(t(lang, "mobile_not_registered"), **LANG_VOICE[lang])
            resp.redirect(f"/api/twilio/aadhar-darshan?lang={lang}")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        gather = resp.gather(
            num_digits=1,
            finishOnKey="#",
            timeout=15,
            action=f"/api/twilio/darshan-date-ask?aadhar={aadhar}&lang={lang}",
            method="POST"
        )
        gather.say(t(lang, "day_prompt"), **LANG_VOICE[lang])

        # fallback if no input
        resp.redirect(f"/api/twilio/darshan-date-ask?aadhar={aadhar}&lang={lang}")

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

class TwilioIVRDarshanDateAsk(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()
        aadhar = request.args.get("aadhar")

        gather = resp.gather(
            num_digits=1,
            timeout=15,
            action=f"/api/twilio/darshan-date-handle?aadhar={aadhar}&lang={lang}",
            method="POST"
        )
        gather.say(t(lang, "day_prompt"), **LANG_VOICE[lang])

        # fallback if no input
        resp.redirect(f"/api/twilio/darshan-date-ask?aadhar={aadhar}&lang={lang}")

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})


class TwilioIVRDarshanConfirm(Resource):
    """
    Final step:
    - all data comes via query params
    - create Passenger
    - generate QR
    - send WhatsApp
    - confirm via voice
    """
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        # ---- Read params (NO Digits here) ----
        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")
        gender = request.args.get("gender")
        age_str = request.args.get("age")
        wheelchair = request.args.get("wheelchair")  # "1" or "0"

        if not all([aadhar, date_str, slot_id, gender, age_str, wheelchair]):
            resp.say(t(lang, "internal_error"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        wheelchair_needed = (wheelchair == "1")

        # ---- Parse values ----
        try:
            age = int(age_str)
            darshan_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            slot_id = int(slot_id)
        except Exception:
            resp.say(t(lang, "internal_error"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # ---- Aadhaar → user ----
        mobile_e164 = AADHAR_MOBILE_MAP.get(aadhar)
        if not mobile_e164:
            resp.say(t(lang, "aadhaar_not_registered"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        user = User.query.filter_by(mobile_no=mobile_e164[-10:]).first()
        if not user:
            resp.say(t(lang, "mobile_not_registered"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # ---- Slot ----
        slot = Aarti_and_DarshanSlot.query.get(slot_id)
        if not slot:
            resp.say(t(lang, "internal_error"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # ---- Capacity ----
        if Passenger.query.filter_by(
            slot_id=slot.id,
            darshan_date=darshan_date
        ).count() >= slot.max_visitors:
            resp.say(t(lang, "slot_full"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # ---- Priority ----
        special = False
        priority = 0

        if age >= 60:
            special = True
            priority += 2 if age >= 70 else 1

        if wheelchair_needed:
            special = True
            priority += 4

        # ---- Create Passenger ----
        passenger = Passenger(
            user_id=user.id,
            slot_id=slot.id,
            darshan_date=darshan_date,
            name=user.name or "Devotee",
            aadhaar_number=aadhar,
            qr_code=None,
            scan_count=0,
            special=special,
            with_special=False,
            age=age,
            gender=gender,
            priority=priority,
            wheelchairneeded=wheelchair_needed
        )

        db.session.add(passenger)
        db.session.flush()

        # ---- QR ----
        metadata = {
            "name": passenger.name,
            "passenger_id": passenger.id,
            "darshan_date": str(darshan_date),
            "slot_id": slot.id,
            "aadhar": aadhar,
            "priority": priority
        }

        # canonical JSON (MUST match scan logic)
        metadata_json = json.dumps(
            metadata,
            sort_keys=True,
            separators=(",", ":")
        )

        # hash
        credential_hash = hashlib.sha256(
            metadata_json.encode()
        ).hexdigest()

        # 🔥 ISSUE ON BLOCKCHAIN (THIS IS THE KEY LINE)
        issue_hash(credential_hash)

        # QR payload
        qr_payload = {
            "metadata": metadata,
            "hash": credential_hash
        }

        qr_data = json.dumps(qr_payload, separators=(",", ":"))

        qr_filename = f"ivr_passenger_{passenger.id}.png"
        passenger.qr_code = qrgenerator(qr_data, qr_filename)

        db.session.commit()

        # ---- WhatsApp (best effort) ----
        try:
            TWILIO_CLIENT.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=f"whatsapp:{mobile_e164}",
                body=(
                    f"Sugam Darshan Ticket #{passenger.id}\n"
                    f"Date: {darshan_date}\n"
                    f"Slot: {slot.start_time.strftime('%I:%M %p')} - "
                    f"{slot.end_time.strftime('%I:%M %p')}\n"
                    f"Radhe Radhe"
                ),
                media_url=[f"{clouflare_url}/api/qrcode/{qr_filename}"]
            )
        except Exception as e:
            print("WhatsApp error:", e)

        # ---- Voice confirm ----
        resp.say(t(lang, "booking_confirm"), **LANG_VOICE[lang])
        resp.hangup()

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})


class TwilioIVRDarshanSlotSelect(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        digit = (request.values.get("Digits") or "").strip()

        # ---- basic sanity ----
        if not aadhar or not date_str:
            resp.say(t(lang, "internal_error"), **LANG_VOICE[lang])
            resp.redirect("/api/twilio/voice")
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        slots = get_ordered_darshan_slots()
        if not slots:
            resp.say(t(lang, "darshan_not_configured"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        # ---- validate input ----
        if not digit.isdigit():
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(
                f"/api/twilio/darshan-slot-ask?"
                f"aadhar={aadhar}&date={date_str}&lang={lang}"
            )
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        idx = int(digit) - 1
        if idx < 0 or idx >= len(slots):
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(
                f"/api/twilio/darshan-slot-ask?"
                f"aadhar={aadhar}&date={date_str}&lang={lang}"
            )
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        slot = slots[idx]

        # ---- NEXT STEP: GENDER ASK (NOT HANDLE) ----
        resp.redirect(
            f"/api/twilio/darshan-gender-ask?"
            f"aadhar={aadhar}"
            f"&date={date_str}"
            f"&slot_id={slot.id}"
            f"&lang={lang}"
        )

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})
        
# class TwilioIVRDarshanGender(Resource):
#     def post(self):
#         resp = VoiceResponse()
#         lang = get_lang()

#         aadhar = request.args.get("aadhar")
#         date_str = request.args.get("date")
#         slot_id = request.args.get("slot_id")
#         digit = (request.values.get("Digits") or "").strip()

#         if digit == "1":
#             gender = "Male"
#         elif digit == "2":
#             gender = "Female"
#         elif digit == "3":
#             gender = "Other"
#         else:
#             resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
#             resp.redirect(
#                 f"/api/twilio/darshan-gender?"
#                 f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}&lang={lang}"
#             )
#             return make_response(str(resp), 200, {"Content-Type": "text/xml"})

#         resp.redirect(
#             f"/api/twilio/darshan-age?"
#             f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
#             f"&gender={gender}&lang={lang}"
#         )
#         return make_response(str(resp), 200, {"Content-Type": "text/xml"})


class TwilioIVRDarshanAge(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")
        gender = request.args.get("gender")

        gather = resp.gather(
            num_digits=2,
            finishOnKey="#",
            timeout=15,
            action=(
                f"/api/twilio/darshan-wheelchair-ask?"
                f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
                f"&gender={gender}&lang={lang}"
            ),
            method="POST"
        )
        gather.say(t(lang, "age_prompt"), **LANG_VOICE[lang])

        resp.redirect(
            f"/api/twilio/darshan-age?"
            f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
            f"&gender={gender}&lang={lang}"
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
            "Radhe Radhe. "
            "For Sugam Darshan ticket booking, press 1. "
            "For Sugam Aarti booking, press 2."
        ),
        "invalid_choice": "Invalid choice.",
        "no_input": "No input received. Restarting.",
        "goodbye": "Radhe Radhe. Goodbye.",
        "aadhaar_prompt": (
            "Please enter your twelve digit Aadhaar number, "
            "followed by the hash key."
        ),
        "aadhaar_not_registered": (
            "This Aadhaar is not registered with Dev Dham Path. "
            "Please register from the app or website. Radhe Radhe."
        ),
        "mobile_not_registered": (
            "Your mobile number is not registered as a user. "
            "Please complete registration from the app. Radhe Radhe."
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
            "Darshan timings are not configured. Please try later. Radhe Radhe."
        ),
        "booking_confirm": (
            "Your Sugam Darshan ticket has been booked successfully. "
            "A WhatsApp confirmation with QR code has been sent to your registered mobile number. "
            "Radhe Radhe."
        ),
    },
    "hi": {
        "lang_select": (
            "Dev Dham Path mein aapka swagat hai. "
            "Hindi ke liye 1 dabaiye. "
            "Angrezi ke liye 2 dabaiye."
        ),
        "main_menu": (
            "Radhe Radhe. "
            "Sugam Darshan ticket booking ke liye 1 dabaiye. "
            "Sugam Aarti booking ke liye 2 dabaiye."
        ),
        "invalid_choice": "Galat vikalp hai.",
        "no_input": "Koi input nahi mila. Phir se koshish karte hain.",
        "goodbye": "Radhe Radhe. Dhanyavaad.",
        "aadhaar_prompt": (
            "Kripya apna baarah ank ka Aadhar number darj karein "
            "aur hash key dabayein."
        ),
        "aadhaar_not_registered": (
            "Yeh Aadhar Dev Dham Path par registered nahi hai. "
            "Kripya app ya website se registration karein. Radhe Radhe."
        ),
        "mobile_not_registered": (
            "Aapka mobile number system mein registered nahi hai. "
            "Kripya app se registration poora karein. Radhe Radhe."
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
            "Kripya baad mein koshish karein. Radhe Radhe."
        ),
        "booking_confirm": (
            "Aapka Sugam Darshan ticket safal roop se buk ho gaya hai. "
            "QR code ke saath WhatsApp par pushti sandesh bhej diya gaya hai. "
            "Radhe Radhe."
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
    
class TwilioIVRDarshanSlotAsk(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")

        slots = get_ordered_darshan_slots()
        if not slots:
            resp.say(t(lang, "darshan_not_configured"), **LANG_VOICE[lang])
            resp.hangup()
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        lines = []
        for i, s in enumerate(slots, start=1):
            start = s.start_time.strftime("%I:%M %p")
            end = s.end_time.strftime("%I:%M %p")
            if lang == "hi":
                lines.append(f"{start} se {end} ke liye {i} dabaiye.")
            else:
                lines.append(f"For {start} to {end}, press {i}.")

        gather = resp.gather(
            num_digits=1,
            timeout=15,
            action=(
                f"/api/twilio/darshan-slot-select?"
                f"aadhar={aadhar}&date={date_str}&lang={lang}"
            ),
            method="POST"
        )
        gather.say(t(lang, "slot_intro") + " " + " ".join(lines), **LANG_VOICE[lang])

        # fallback ONLY to ASK
        resp.redirect(
            f"/api/twilio/darshan-slot-ask?"
            f"aadhar={aadhar}&date={date_str}&lang={lang}"
        )

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

class TwilioIVRDarshanWheelchairAsk(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")
        gender = request.args.get("gender")
        age = (request.values.get("Digits") or "").strip()

        if not age.isdigit() or not (1 <= int(age) <= 120):
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(
                f"/api/twilio/darshan-age?"
                f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
                f"&gender={gender}&lang={lang}"
            )
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        gather = resp.gather(
            num_digits=1,
            finishOnKey="#",
            timeout=15,
            action=(
                f"/api/twilio/darshan-wheelchair-handle?"
                f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
                f"&gender={gender}&age={age}&lang={lang}"
            ),
            method="POST"
        )
        gather.say(t(lang, "wheelchair_prompt"), **LANG_VOICE[lang])

        resp.redirect(
            f"/api/twilio/darshan-wheelchair-ask?"
            f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
            f"&gender={gender}&lang={lang}"
        )

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

class TwilioIVRDarshanWheelchairHandle(Resource):
    def post(self):
        resp = VoiceResponse()
        wc = (request.values.get("Digits") or "").strip()

        if wc not in ("1", "2"):
            resp.say("Invalid choice.")
            resp.redirect(request.url)
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        resp.redirect(
            f"/api/twilio/darshan-confirm?"
            f"{request.query_string.decode()}&wheelchair={wc}"
        )
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

class TwilioIVRDarshanGenderAsk(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")

        gather = resp.gather(
            num_digits=1,
            timeout=15,
            action=(
                f"/api/twilio/darshan-gender-handle?"
                f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}&lang={lang}"
            ),
            method="POST"
        )
        gather.say(t(lang, "gender_prompt"), **LANG_VOICE[lang])

        # fallback ONLY to ASK
        resp.redirect(
            f"/api/twilio/darshan-gender-ask?"
            f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}&lang={lang}"
        )

        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

class TwilioIVRDarshanGenderHandle(Resource):
    def post(self):
        resp = VoiceResponse()
        lang = get_lang()

        aadhar = request.args.get("aadhar")
        date_str = request.args.get("date")
        slot_id = request.args.get("slot_id")
        digit = (request.values.get("Digits") or "").strip()

        if digit == "1":
            gender = "Male"
        elif digit == "2":
            gender = "Female"
        elif digit == "3":
            gender = "Other"
        else:
            resp.say(t(lang, "invalid_choice"), **LANG_VOICE[lang])
            resp.redirect(
                f"/api/twilio/darshan-gender-ask?"
                f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}&lang={lang}"
            )
            return make_response(str(resp), 200, {"Content-Type": "text/xml"})

        resp.redirect(
            f"/api/twilio/darshan-age?"
            f"aadhar={aadhar}&date={date_str}&slot_id={slot_id}"
            f"&gender={gender}&lang={lang}"
        )
        return make_response(str(resp), 200, {"Content-Type": "text/xml"})

    
api.add_resource(TwilioIVRStart, "/twilio/voice")
api.add_resource(TwilioIVRLanguageSelect, "/twilio/lang-select")
api.add_resource(TwilioIVRMenu, "/twilio/menu")
api.add_resource(TwilioIVRAadhaarDarshan, "/twilio/aadhar-darshan")
api.add_resource(TwilioIVRAadhaarDarshanVerify, "/twilio/aadhar-darshan-verify")
api.add_resource(TwilioIVRDarshanDateAsk, "/twilio/darshan-date-ask")
api.add_resource(TwilioIVRDarshanSlotAsk, "/twilio/darshan-slot-ask")
api.add_resource(TwilioIVRDarshanSlotSelect, "/twilio/darshan-slot-select")
api.add_resource(TwilioIVRDarshanAge, "/twilio/darshan-age")
api.add_resource(TwilioIVRDarshanWheelchair, "/twilio/darshan-wheelchair")
api.add_resource(TwilioIVRDarshanConfirm, "/twilio/darshan-confirm")
api.add_resource(TwilioIVRDarshanDateHandle, "/twilio/darshan-date-handle")
api.add_resource(TwilioIVRDarshanWheelchairAsk, "/twilio/darshan-wheelchair-ask")
api.add_resource(TwilioIVRDarshanWheelchairHandle, "/twilio/darshan-wheelchair-handle")
api.add_resource(TwilioIVRDarshanGenderAsk, "/twilio/darshan-gender-ask")
api.add_resource(TwilioIVRDarshanGenderHandle, "/twilio/darshan-gender-handle")





emergency_bp = Blueprint('emergency', __name__, url_prefix='/api/emergency')

# In-memory queue (no DB)
# Only last 100 alerts kept in memory
ALERT_BUFFER = deque(maxlen=100)

# Temple geo-fence config
TEMPLE_LAT = 20.8880
TEMPLE_LNG = 50.4012
MAX_RADIUS = 500  # meters


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def make_alert_from_payload(data, *, location=None, inside_geofence=None, distance_m=None):
    """
    Build the alert dict that will be stored in ALERT_BUFFER.
    Now also includes `emergency_type` so Admin UI can display it.
    """
    if location is None:
        location = (data.get('location') or {}) or {}

    # 🔴 Support both `timestamp` and `timestamp_utc` from frontend
    ts = None
    if data.get('timestamp_utc'):
        try:
            ts = datetime.fromisoformat(
                data['timestamp_utc'].replace('Z', '+00:00')
            )
        except Exception:
            ts = None

    if ts is None and data.get('timestamp'):
        try:
            ts = datetime.fromisoformat(
                data['timestamp'].replace('Z', '+00:00')
            )
        except Exception:
            ts = None

    if ts is None:
        ts = datetime.now(timezone.utc)

    ts_utc = ts.astimezone(timezone.utc)

    # ✅ Read emergency_type from payload
    emergency_type = (
        data.get("emergency_type")
        or data.get("type")
        or data.get("sos_type")
    )

    return {
        "id": str(uuid.uuid4()),
        "user_id": data.get("user_id"),
        "user_name": data.get("user_name"),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "accuracy": location.get("accuracy"),
        "timestamp_utc": ts_utc.isoformat(),
        "current_page": data.get("current_page"),
        "status": data.get("status") or "PENDING",
        "received_at": datetime.now(timezone.utc).isoformat(),
        "inside_geofence": inside_geofence,
        "distance_m": distance_m,
        # 👇 NEW FIELD – this is what Admin/Guard dashboards use
        "emergency_type": emergency_type,
    }


@emergency_bp.route('/trigger', methods=['POST'])
def trigger_emergency():
    try:
        data = request.get_json() or {}

        # ✅ Support BOTH formats from frontend:
        # 1) { location: { latitude, longitude } }
        # 2) { latitude, longitude }
        loc = (data.get('location') or {}) or {}
        raw_lat = loc.get('latitude', data.get('latitude'))
        raw_lng = loc.get('longitude', data.get('longitude'))

        # Default: assume no location / no geofence
        inside = None
        distance = None
        clean_location = {
            "latitude": None,
            "longitude": None,
            "accuracy": None,
        }

        if raw_lat is not None and raw_lng is not None:
            try:
                lat = float(raw_lat)
                lng = float(raw_lng)

                distance = calculate_distance(lat, lng, TEMPLE_LAT, TEMPLE_LNG)
                inside = distance <= MAX_RADIUS

                clean_location = {
                    "latitude": lat,
                    "longitude": lng,
                    "accuracy": loc.get("accuracy"),
                }
            except (TypeError, ValueError):
                print("❌ Invalid latitude/longitude in SOS payload:", raw_lat, raw_lng)

        # ⚠️ Make sure `emergency_type` from frontend is passed through as-is
        # (it's already in `data`, so make_alert_from_payload will pick it up)
        alert = make_alert_from_payload(
            data,
            location=clean_location,
            inside_geofence=inside,
            distance_m=distance,
        )

        ALERT_BUFFER.appendleft(alert)

        print("🚨 NEW EMERGENCY ALERT:", alert)

        return jsonify({
            "success": True,
            "message": "SOS received",
            "alert_id": alert["id"],
            "inside_geofence": inside,
            "distance_m": distance,
        }), 201

    except Exception as e:
        print("❌ Error in /api/emergency/trigger:", repr(e))
        return jsonify({
            "success": False,
            "message": "Internal server error in SOS trigger",
            "error": str(e),
        }), 500

@emergency_bp.route('/triggerforces',methods=['POST'])
def force_emergency():
    data= request.get_json()
    emergency=data.get("emergency_type")
    message = TWILIO_SMS_CLIENT.messages.create(
                from_=TWILIO_SMS_NUMBER,
                body=emergency,
                to=POLICE_NUMBER,)
    return jsonify({"success": True, "message": "Force SOS sent to police"}), 201
@emergency_bp.route('/admin/alerts', methods=['GET'])
def get_emergency_alerts():
    """
    Admin dashboard uses this.
    We just dump ALERT_BUFFER – each alert now includes `emergency_type`.
    """
    return jsonify(list(ALERT_BUFFER))


@emergency_bp.route('/clear', methods=['POST'])
def clear_sos_alerts():
    ALERT_BUFFER.clear()
    print("⚠️ All SOS alerts cleared from memory")
    return jsonify({"success": True, "message": "All SOS alerts cleared"})


@emergency_bp.route('/send-to-security', methods=['POST'])
def send_to_security():
    """
    Admin clicks 'Send to Security Officer'
    -> mark alert as IN_PROGRESS in the in-memory buffer.
    -> send SMS to security officer via Twilio.
    """
    data = request.get_json() or {}
    alert_id = data.get("alert_id")

    if not alert_id:
        return jsonify({"success": False, "message": "alert_id is required"}), 400

    alert_id = str(alert_id)

    for alert in ALERT_BUFFER:
        if str(alert.get("id")) == alert_id:
            alert["status"] = "IN_PROGRESS"
            alert["sent_to_security_at"] = datetime.now(timezone.utc).isoformat()
            print("📨 Alert sent to security:", alert)

            # 🔔 NEW: fire Twilio SMS here
            send_sms_to_security(alert)

            return jsonify({"success": True, "alert": alert}), 200

    return jsonify({"success": False, "message": "Alert not found"}), 404

@emergency_bp.route('/security/alerts', methods=['GET'])
def get_security_alerts():
    """
    Security dashboard polls this.
    Return only alerts that are sent to security (IN_PROGRESS).
    """
    security_alerts = [
        alert for alert in ALERT_BUFFER
        if alert.get("status") == "IN_PROGRESS"
    ]
    return jsonify(security_alerts), 200

def send_sms_to_security(alert: dict):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SMS_NUMBER, SECURITY_OFFICER_NUMBER]):
        print("⚠️ Twilio env variables not set. Skipping SMS send.")
        return

    try:

        emergency_type = alert.get("emergency_type") or "Unknown"
        user_name = alert.get("user_name") or "Unknown Devotee"
        user_id = alert.get("user_id") or "N/A"

        lat = alert.get("latitude")
        lng = alert.get("longitude")

        if lat and lng:
            location_text = f"Location: {lat:.5f}, {lng:.5f}"
        else:
            location_text = "Location: Not available"

        body = (
            "🚨 TEMPLE SOS ALERT 🚨\n"
            f"Type: {emergency_type}\n"
            f"Devotee: {user_name} (ID: {user_id})\n"
            f"{location_text}\n"
            "Please check the security console for full details."
        )

        message = TWILIO_SMS_CLIENT.messages.create(
            from_=TWILIO_SMS_NUMBER,
            body=body,
            to=SECURITY_OFFICER_NUMBER,
        )

        print("✅ Twilio SMS sent to security officer. SID:", message.sid)

    except Exception as e:
        print("❌ Failed to send Twilio SMS to security officer:", repr(e))

@emergency_bp.route('/resolve', methods=['POST'])
def resolve_alert():
    """
    Security guard clicks 'Acknowledge'
    -> mark alert as RESOLVED.
    """
    data = request.get_json() or {}
    alert_id = data.get("alert_id")

    if not alert_id:
        return jsonify({"success": False, "message": "alert_id is required"}), 400

    alert_id = str(alert_id)

    for alert in ALERT_BUFFER:
        if str(alert.get("id")) == alert_id:
            alert["status"] = "RESOLVED"
            alert["resolved_at"] = datetime.now(timezone.utc).isoformat()
            print("✅ Alert resolved by security:", alert)
            return jsonify({"success": True, "alert": alert}), 200

    return jsonify({"success": False, "message": "Alert not found"}), 404
