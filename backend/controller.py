import ast
from flask import request,current_app as app,make_response,send_from_directory
from flask_restful import Api,Resource,fields, marshal_with,marshal
from models.model import *
import mimetypes
import os
import requests
import calendar
import base64 as Base64
import time
import random
from datetime import datetime
from werkzeug.utils import secure_filename
import qrcode
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
api=Api(prefix='/api')
otp_login_storage = {}

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
            msg=TWILIO_CLIENT.messages.create(
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

        if not all([name, email, password, pincode, address]):
            return {"message": "All fields are required"}, 400

        # Check duplicate
        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered"}, 409

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
        for r in user.reservations:  # assuming relationship exists
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
            "address": user.address
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

        db.session.commit()
        return {"message": "Profile updated successfully"}, 200

api.add_resource(UserProfileResource, '/user/<int:user_id>')



class ImageserverResource(Resource):
    def get(self, filename):
        base_path = os.path.abspath(os.path.join(app.root_path, '..', 'static', 'qrcode'))
        response = make_response(send_from_directory(base_path, filename))
        response.headers['Content-Type'] = mimetypes.guess_type(filename)[0] or 'image/png'
        return response
api.add_resource(ImageserverResource,'/qrcode/<string:filename>')



# -------------------------------------------
#  TWILIO + OTP STORAGE (UNCHANGED)
# -------------------------------------------
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
CONTENT_SID = os.getenv("CONTENT_SID")

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

# -------------------------------------------
#  SEND OTP (UNCHANGED)
# -------------------------------------------
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


api.add_resource(SendOtpResource, '/send-otp')


# -------------------------------------------
#  VERIFY OTP (UNCHANGED)
# -------------------------------------------
class VerifyOtpResource(Resource):
    def post(self):
        data = request.get_json()
        aadhar = data.get("aadhar")
        otp = data.get("otp")

        stored = otp_storage.get(aadhar)
        if stored and stored == otp:
            return {"success": True, "message": "OTP Verified"}, 200

        return {"success": False, "message": "Invalid OTP"}, 400


api.add_resource(VerifyOtpResource, '/verify-otp')


# -------------------------------------------
#  GET BOOK TICKET PAGE DATA (MANDIR REMOVED)
# -------------------------------------------
class BookTicketDataResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        slots = DarshanSlot.query.order_by(DarshanSlot.start_time).all()
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
        slot = DarshanSlot.query.get(slot_id)

        if not user or not slot:
            return {"success": False, "message": "Invalid user or slot"}, 400

        try:
            selected_date = datetime.strptime(darshan_date, "%Y-%m-%d").date()
        except:
            return {"success": False, "message": "Invalid date format"}, 400

        num_members = len(passengers)

        already_booked = db.session.query(Passenger)\
            .join(Booking)\
            .filter(
                Booking.slot_id == slot_id,
                Booking.darshan_date == selected_date
            ).count()

        if already_booked + num_members > slot.max_visitors:
            return {
                "success": False,
                "message": f"Only {slot.max_visitors - already_booked} slots left"
            }, 400

        booking = Booking(
            user_id=user_id,
            slot_id=slot_id,
            darshan_date=selected_date,
            total_passengers=num_members
        )
        db.session.add(booking)
        db.session.flush()

        QR_FOLDER = os.path.join("static", "qrcode")
        os.makedirs(QR_FOLDER, exist_ok=True)

        booked_passengers = []

        for p in passengers:
            name = p.get("name")
            aadhar = p.get("aadhar")
            otp_entered = p.get("otp")

            if otp_storage.get(aadhar) != otp_entered:
                return {"success": False, "message": f"OTP failed for {name}"}, 400

            otp_storage.pop(aadhar, None)

            passenger = Passenger(
                booking_id=booking.id,
                name=name,
                aadhaar_number=aadhar
            )
            db.session.add(passenger)
            db.session.flush()

            qr_data = str({"name":name,"passenger_id":passenger.id, "darshan_date":darshan_date, "slot_id":slot_id,"adhaar":aadhar})
            qr_data_bytes=qr_data.encode('utf-8')
            qr_data=Base64.b64encode(qr_data_bytes)
            qr_img = qrcode.make(qr_data)
            qr_filename = f"passenger_{passenger.id}_{secure_filename(name)}.png"
            qr_path = os.path.join(QR_FOLDER, qr_filename)
            qr_img.convert('RGB').save(qr_path, 'PNG')

            passenger.qr_code = qr_data
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
                    media_url=[f"https://senators-indexes-finger-gui.trycloudflare.com/api/qrcode/{qr_filename}"],
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
            "booking_id": booking.id,
            "passengers": booked_passengers
        }, 200

api.add_resource(BookTicketResource, '/book-ticket')
# -------------------------------------------
API_USER = os.getenv("CALANDER_UID")
API_KEY = os.getenv("CALANDER_API_KEY")

class PanchangMonthResource(Resource):
    def post(self):
        data = request.get_json()
        month = data["month"]
        year = data["year"]

        total_days = calendar.monthrange(year, month)[1]

        result = {}

        for day in range(1, total_days + 1):

            # 1. Check cache
            cached = PanchangCache.query.filter_by(
                day=day, month=month, year=year
            ).first()

            if cached:
                result[day] = cached.tithi
                continue

            # 2. Call Astrology API if not cached
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

            # 3. Save in DB
            new_entry = PanchangCache(
                day=day,
                month=month,
                year=year,
                tithi=tithi
            )
            db.session.add(new_entry)
            db.session.commit()

            result[day] = tithi

        return result, 200


api.add_resource(PanchangMonthResource, "/calender/month")