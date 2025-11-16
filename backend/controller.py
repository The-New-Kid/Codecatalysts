import ast
from flask import request,current_app as app
from flask_restful import Api,Resource,fields, marshal_with,marshal
from models.model import *

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
