import ast
from flask import request,current_app as app,make_response,send_from_directory
from flask_restful import Api,Resource,fields, marshal_with,marshal
from models.model import *
import mimetypes
import os
api=Api(prefix='/api')


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

        if not all([name, email, password, pincode, address]):
            return {"message": "All fields are required"}, 400

        # Check duplicate
        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered"}, 409

        # Create user
        new_user = User(name=name, email=email, password=password,
                        pincode=pincode, address=address)
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
#  IMPORTS FOR NEW FEATURES (SAFE TO ADD)
# -------------------------------------------
import random
from datetime import datetime
from werkzeug.utils import secure_filename
import qrcode
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------
#  TWILIO + OTP STORAGE
# -------------------------------------------
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
CONTENT_SID = os.getenv("CONTENT_SID")

TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

AADHAR_MOBILE_MAP = {
    "111122223333": "+917042213383",
    "222233334444": "+919812345678",
    "333344445555": "+919900112233",
    "444455556666": "+919988776655",
    "555566667777": "+919911223344",
    "666677778888": "+919922334455",
}

otp_storage = {}


# -------------------------------------------
#  SEND OTP (WHATSAPP)
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
#  VERIFY OTP
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
#  GET BOOK TICKET PAGE DATA
# -------------------------------------------
class BookTicketDataResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        slots = DarshanSlot.query.order_by(DarshanSlot.start_time).all()
        lots = ParkingLot.query.all()
        mandirs = Mandir.query.all()

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
            ],
            "mandirs": [
                {"id": m.id, "name": m.name} for m in mandirs
            ]
        }, 200


api.add_resource(BookTicketDataResource, '/book-ticket/<int:user_id>')


# -------------------------------------------
#  BOOK TICKET (POST)
# -------------------------------------------
class BookTicketResource(Resource):
    def post(self):
        data = request.get_json()
        print("Booking Data:", data)
        user_id = data.get("user_id")
        slot_id = data.get("slot_id")
        passengers = data.get("passengers")
        mobile_number = data.get("mobile_number")

        user = User.query.get(user_id)
        slot = DarshanSlot.query.get(slot_id)

        if not user or not slot:
            return {"success": False, "message": "Invalid user or slot"}, 400

        num_members = len(passengers)

        # Capacity Check
        booked = Ticket.query.filter_by(slot_id=slot_id).count()
        if booked + num_members > slot.max_visitors:
            return {
                "success": False,
                "message": f"Only {slot.max_visitors - booked} slots left"
            }, 400

        # QR folder
        QR_FOLDER = os.path.join("static", "qrcode")
        os.makedirs(QR_FOLDER, exist_ok=True)

        booked_tickets = []

        for p in passengers:
            name = p["name"]
            aadhar = p["aadhar"]
            otp_entered = p["otp"]

            # OTP Check
            if otp_storage.get(aadhar) != otp_entered:
                return {"success": False, "message": f"OTP failed for {name}"}, 400

            otp_storage.pop(aadhar, None)

            # Create Ticket
            ticket = Ticket(user_id=user_id, slot_id=slot_id)
            db.session.add(ticket)
            db.session.commit()

            # Generate QR Code
            qr_data = str(ticket.id)
            qr_img = qrcode.make(qr_data)
            qr_filename = f"ticket_{ticket.id}_{secure_filename(name)}.png"
            qr_path = os.path.join(QR_FOLDER, qr_filename)
            img_rgb = qr_img.convert('RGB')
            img_rgb.save(qr_path, 'PNG')

            ticket.qr_code = qr_filename
            db.session.commit()


            # WhatsApp Ticket
            try:
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=f"Ticket #{ticket.id} booked for {name} at {slot.start_time.strftime('%Y-%m-%d %H:%M')}",
                    to=f"whatsapp:{"+91"+mobile_number}"
                )

                TWILIO_CLIENT.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=f"Ticket #{ticket.id} booked for {name} at {slot.start_time.strftime('%Y-%m-%d %H:%M')}",
                media_url=[f"https://sally-rating-incidents-sally.trycloudflare.com/api/qrcode/{qr_filename}"],
                to=f"whatsapp:+91{mobile_number}"
                )

            except Exception as e:
                print("WhatsApp Error:", e)

            booked_tickets.append({
                "ticket_id": ticket.id,
                "qr_code": ticket.qr_code
            })

        return {"success": True, "tickets": booked_tickets}, 200


api.add_resource(BookTicketResource, '/book-ticket')