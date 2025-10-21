from flask import session,Flask,render_template,request,url_for,redirect,flash,jsonify
COUNTRY = "IN"
import requests
from models.model import *
from sqlalchemy import or_
from flask import current_app as app
from datetime import datetime,date,timedelta
from sqlalchemy import func
from functools import wraps
import qrcode,calendar,random
import io
from twilio.rest import Client  
import base64,os,json
from werkzeug.utils import secure_filename
from PIL import Image
from pyzbar.pyzbar import decode
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
AADHAR_MOBILE_MAP = {
    "111122223333": "+919696733181",
    "222233334444": "+919812345678",
    "333344445555": "+919900112233",
    "444455556666": "+919988776655",
    "555566667777": "+919911223344",
    "666677778888": "+919922334455"
}
otp_storage = {} 
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
CONTENT_SID = os.getenv("CONTENT_SID")

def get_density(festival=False, weekend=False):
    if festival:
        return "High", "red"
    elif weekend:
        return "Medium", "yellow"
    else:
        return "Low", "green"

def login_required(role=None):
    """
    Protect routes:
    role=None -> any logged-in user
    role=0 -> admin only
    role=1 -> user only
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check session
            user_id = session.get('user_id')
            user_role = session.get('role')

            if not user_id:
                flash("You must login first.", "warning")
                return redirect(url_for("signin"))

            if role is not None and user_role != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("signin"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login" ,methods=["GET","POST"])
def signin():
    session.clear()
    if request.method=="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        usr = User.query.filter_by(email=email, password=password).first()
        if usr:
            session['user_id'] = usr.id
            session['role'] = usr.role  # 0 = admin, 1 = user
            flash("Login successful!", "success")
            if usr.role == 0: 
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("user_dashboard", user_id=usr.id))
        flash("Invalid username or password", "danger")
        return redirect(url_for("signin"))
    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password") 
        email=request.form.get("email")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        usr=User.query.filter_by(email=email).first()
        if usr:
            flash("Sorry, this mail already registered!!!","danger")
            return redirect(url_for("signup"))
        new_usr=User(name=name,email=email,password=password,pincode=pincode,address=address)
        db.session.add(new_usr)
        db.session.commit()
        flash("Registration Successful","success")
        return redirect(url_for("signin"))
    return render_template("register.html")

@app.route('/admin_dashboard')
@login_required(role=0)
def admin_dashboard():
    query = request.args.get('q', '').strip()
    if query:
        search = f"%{query}%"
        parking_lots = ParkingLot.query.filter(
            ParkingLot.prime_location_name.ilike(search),
            ParkingLot.is_private==False
        ).all()
    else:
        parking_lots = ParkingLot.query.filter_by(is_private=False).all()
    for lot in parking_lots:
        total = lot.max_spots
        normal_count = int(0.6 * total)
        extra_count = int(0.3 * total)
        vip_count = int(0.1 * total)
        assigned = normal_count + extra_count + vip_count
        remainder = total - assigned
        extra_count += remainder
        colored_spots = []
        for idx, spot in enumerate(lot.spots):
            if idx < normal_count:
                colored_spots.append({'status': spot.status, 'color': 'green', 'id': spot.id})
            elif idx < normal_count + extra_count:
                colored_spots.append({'status': spot.status, 'color': 'grey', 'id': spot.id})
            else:
                colored_spots.append({'status': spot.status, 'color': 'pink', 'id': spot.id})
        lot.colored_spots = colored_spots

    return render_template('admin_dashboard.html', parking_lots=parking_lots, query=query)

@app.route("/add_lot", methods=["GET","POST"])
@login_required(role=0)
def add_lot():
    if request.method == 'POST':
        prime_location_name = request.form.get('prime_location_name')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        price_per_hour = request.form.get('price_per_hour')
        max_spots = int(request.form.get('max_spots'))
        new_lot = ParkingLot(
            prime_location_name=prime_location_name,
            address=address,
            pin_code=pin_code,
            price_per_hour=price_per_hour,
            max_spots=max_spots
        )
        db.session.add(new_lot)
        db.session.commit()
        for i in range(max_spots):
            spot = ParkingSpot(status='A', lot_id=new_lot.id)
            db.session.add(spot)
        db.session.commit()
        flash('Parking Lot Added Successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_lot.html')

@app.route('/private_parking')
@login_required(role=0)
def private_parking():
    private_lots = ParkingLot.query.filter_by(is_private=True).all()
    return render_template('private_parking.html', private_lots=private_lots)

@app.route('/add_private_lot', methods=['GET', 'POST'])
@login_required(role=0)
def add_private_lot():
    if request.method == 'POST':
        prime_location_name = request.form['prime_location_name']
        address = request.form['address']
        pin_code = request.form['pin_code']
        price_per_hour = request.form['price_per_hour']
        max_spots = int(request.form['max_spots'])

        # create a new Lot with is_private=True
        new_lot = ParkingLot(
            prime_location_name=prime_location_name,
            address=address,
            pin_code=pin_code,
            price_per_hour=price_per_hour,
            max_spots=max_spots,
            is_private=True   # 👈 differentiate
        )

        db.session.add(new_lot)
        db.session.commit()
        for i in range(max_spots):
            spot = ParkingSpot(status='A', lot_id=new_lot.id)
            db.session.add(spot)
        db.session.commit()

        flash('Private Parking Lot Added Successfully!', 'success')
        return redirect(url_for('private_parking'))
    return render_template('add_private_lot.html')



@app.route('/admin/parking-lot/<int:lot_id>/delete', methods=['POST'])
@login_required(role=0)
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    for spot in lot.spots:
        if spot.status == 'O':
            flash("Occupied lot can't be deleted", "danger")
            return redirect(url_for('admin_dashboard'))
    for spot in lot.spots:
        reservations = Reservation.query.filter_by(spot_id=spot.id).all()
        for res in reservations:
            db.session.delete(res)
        db.session.delete(spot)
    db.session.delete(lot)
    db.session.commit()
    if lot.is_private:
        return redirect(url_for('private_parking'))
    else:
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/parking-lot/<int:lot_id>/edit', methods=['GET', 'POST'])
@login_required(role=0)
def edit_parking_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if request.method == 'POST':
        occupied_spots = sum(1 for spot in lot.spots if spot.status == 'O')
        current_total_spots = len(lot.spots)
        new_max = int(request.form.get('max_spots'))
        if new_max < occupied_spots:
            flash(f" Max spots is less than occupied", "danger")
            return redirect(url_for('edit_parking_lot', lot_id=lot.id))
        lot.prime_location_name = request.form.get('prime_location_name')
        lot.address = request.form.get('address')
        lot.pin_code = request.form.get('pin_code')
        lot.price_per_hour = request.form.get('price_per_hour')
        lot.max_spots = new_max
        if new_max > current_total_spots:
            for i in range(new_max - current_total_spots):
                new_spot = ParkingSpot(lot_id=lot.id, status='A')
                db.session.add(new_spot)
        elif new_max < current_total_spots:
            extra_spots = [spot for spot in lot.spots if spot.status == 'A']
            to_remove = current_total_spots - new_max
            for spot in extra_spots[:to_remove]:
                db.session.delete(spot)
        db.session.commit()
        flash("Parking lot updated successfully.", "success")
        if lot.is_private:
            return redirect(url_for('private_parking'))
        else:
            return redirect(url_for('admin_dashboard'))
    return render_template('editlot.html', lot=lot)

@app.route("/admin/users")
@login_required(role=0)
def view_users():
    query = request.args.get('q', '').strip()
    if query:
        search = f"%{query}%"
        users = User.query.filter(
            or_(
                func.lower(User.name).ilike(search),
                func.cast(User.id, db.String).ilike(search)
            )
        ).all()
    else:
        users = User.query.filter_by(role=1).all()
    return render_template('admin_users.html', users=users, query=query)

@app.route('/admin/summary')
@login_required(role=0)
def summary():
    total_spots = ParkingSpot.query.count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    vacant_spots = total_spots - occupied_spots
    lots = ParkingLot.query.all()
    lot_names = [lot.prime_location_name for lot in lots]
    revenues = [round(lot.revenue or 0, 2) for lot in lots]
    total_revenue = sum(revenues)
    return render_template(
        "admin_summary.html",
        total_spots=total_spots,
        occupied_spots=occupied_spots,
        vacant_spots=vacant_spots,
        lot_names=lot_names,
        revenues=revenues,
        total_revenue=round(total_revenue, 2)
    )

@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required(role=0)
def edit_profile():
    admin = User.query.filter_by(role=0).first()
    if request.method == 'POST':
        admin.name = request.form.get("name")
        admin.password=request.form.get("password")
        admin.email =request.form.get("email")
        admin.pincode = request.form.get("pincode")
        admin.address = request.form.get("address")
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('edit_profile'))
    return render_template('admin_edit_profile.html', admin=admin)

@app.route('/spot/<int:spot_id>')
@login_required(role=0)
def spot_detail(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    lot = spot.lot
    if not lot.is_private:
        total = lot.max_spots
        normal_count = int(0.6 * total)
        extra_count = int(0.3 * total)
        vip_count = int(0.1 * total)
        assigned = normal_count + extra_count + vip_count
        remainder = total - assigned
        extra_count += remainder
        spot_index = lot.spots.index(spot)
        if spot_index < normal_count:
            spot.color = 'green'
        elif spot_index < normal_count + extra_count:
            spot.color = 'grey'
        else:
            spot.color = 'pink'
    else:
        spot.color = 'green'
    return render_template('spot_detail.html', spot=spot, lot=lot)

@app.route('/delete_spot/<int:spot_id>', methods=['POST'])
@login_required(role=0)
def delete_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    if spot.status != 'A':
        flash('Cannot delete: This spot is currently occupied.', 'danger')
        return redirect(url_for('spot_detail', spot_id=spot.id))
    lot=spot.lot
    lot.max_spots-=1
    db.session.delete(spot)
    db.session.commit()
    flash(' Spot deleted successfully.', 'success')
    if lot.is_private:
        return redirect(url_for('private_parking'))
    else:
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/spot/<int:spot_id>/details')
@login_required(role=0)
def occupied_spot_details(spot_id):
    spot = ParkingSpot.query.get(spot_id)
    reservation = Reservation.query.filter_by(spot_id=spot.id).order_by(Reservation.id.desc()).first()
    user = User.query.get(reservation.user_id)
    return render_template('occupied_spot_details.html', spot=spot, reservation=reservation, user=user)

@app.route("/user_dashboard/<int:user_id>")
@login_required(role=1)
def user_dashboard(user_id):
    user = User.query.get_or_404(user_id)
    
    reservations = (
        Reservation.query
        .filter_by(user_id=user.id)
        .join(ParkingSpot)
        .join(ParkingLot)
        .order_by(Reservation.parking_timestamp.desc())
        .all()
    )
    valid_reservations = [r for r in reservations if r.spot and r.spot.lot]
    lots = ParkingLot.query.all()
    lot_availability = []
    for lot in lots:
        total_spots = lot.max_spots
        if lot.is_private:
            available_spots=sum(1 for spot in lot.spots if spot.status=='A')
        else:
            normal_count = int(0.6 * total_spots)
            extra_count = int(0.3 * total_spots)
            vip_count = int(0.1 * total_spots)

            # handle remainder
            assigned = normal_count + extra_count + vip_count
            remainder = total_spots - assigned
            extra_count += remainder  # Extra gets priority

        # Only count visible (normal) spots
            available_spots = sum(
            1 for idx, spot in enumerate(lot.spots) 
            if idx < normal_count and spot.status == 'A'
            )
        lot_availability.append({
            'lot_id': lot.id,
            'lot_name': lot.prime_location_name,
            'address': lot.address,
            'available_spots': available_spots
        })
    return render_template(
        "user_dashboard.html", 
        user=user, 
        reservations=valid_reservations,
        lots=lot_availability
    )

@app.route("/user/public_lots/<int:user_id>")
@login_required(role=1)
def user_public_lots(user_id):
    user = User.query.get_or_404(user_id)
    lots = ParkingLot.query.filter_by(is_private=False).all()
    
    public_lots = []
    for lot in lots:
        total_spots = lot.max_spots or 0

        # determine visible(normal) capacity: use 60% but ensure at least 1 if total>0
        normal_count = int(0.6 * total_spots)
        if total_spots > 0 and normal_count == 0:
            normal_count = 1

        # make sure counts sum <= total (give remainder to extra)
        extra_count = int(0.2 * total_spots)
        vip_count = total_spots - (normal_count + extra_count)
        if vip_count < 0:  # adjust if rounding caused negative
            vip_count = 0
            extra_count = total_spots - normal_count

        # sort spots by id to keep deterministic order
        sorted_spots = sorted(lot.spots, key=lambda s: s.id)
        # count available only among the first normal_count spots (the green ones)
        available_normal = sum(
            1 for idx, spot in enumerate(sorted_spots)
            if idx < normal_count and spot.status == 'A'
        )
        percent = (available_normal / normal_count) if normal_count > 0 else 0
        public_lots.append({
            'lot_id': lot.id,
            'lot_name': lot.prime_location_name,
            'address': lot.address,
            'available_spots': available_normal,
            'visible_capacity': normal_count,
            'available_percent': int(round(percent * 100))
        })
    return render_template("user_public.html", user=user, lots=public_lots)



# Private availability page
@app.route("/user/private_lots/<int:user_id>")
@login_required(role=1)
def user_private_lots(user_id):
    user = User.query.get_or_404(user_id)
    lots = ParkingLot.query.filter_by(is_private=True).all()
    private_lots = []
    for lot in lots:
        available_spots = sum(1 for spot in lot.spots if spot.status == 'A')
        private_lots.append({
            'lot_id': lot.id,
            'lot_name': lot.prime_location_name,
            'address': lot.address,
            'available_spots': available_spots
        })
    return render_template("user_private.html", user=user, lots=private_lots)

@app.route("/user/book/<int:user_id>", methods=["GET","POST"])
@login_required(role=1)
def book_spot(user_id):
    user = User.query.get(user_id)
    lot_type = request.args.get("lot_type", "public")  # default to public

    if request.method == "POST":
        lot_id = request.form.get("lot_id")
        vehicle_number = request.form.get("vehicle_number")
        if not lot_id or not vehicle_number:
            flash("Please select a location and enter vehicle number.", "warning")
            return redirect(url_for("book_spot", user_id=user.id, lot_type=lot_type))
        
        lot = ParkingLot.query.get(lot_id)
        total_spots = lot.max_spots
        green_limit = int(0.6 * total_spots)  # only first 60% are green

        # Get the first available green spot
        spot = None
        for idx, s in enumerate(lot.spots):
            if idx < green_limit and s.status == 'A':  # only green spots
                spot = s
                break
        
        if not spot:
            flash("No available green spots for booking in this lot.", "danger")
            return redirect(url_for("book_spot", user_id=user.id, lot_type=lot_type))

        # Book the spot
        new_reservation = Reservation(
            spot_id=spot.id,
            user_id=user.id,
            vehicle_number=vehicle_number,
            parking_timestamp=datetime.now(),
            cost_per_hour=lot.price_per_hour
        )
        spot.status = 'O'
        db.session.add(new_reservation)
        db.session.commit()
        flash("Booking confirmed!", 'success')
        return redirect(url_for("user_dashboard", user_id=user.id))
    if lot_type == "private":
        lots = ParkingLot.query.filter_by(is_private=True).all()
    else:
        lots = ParkingLot.query.filter_by(is_private=False).all()
    return render_template("user_book_spot.html", user=user, lots=lots, lot_type=lot_type)

@app.route("/release/<int:reservation_id>/<int:user_id>", methods=["POST"])
@login_required(role=1)
def release_spot(reservation_id, user_id):
    reservation = Reservation.query.get(reservation_id)
    user=User.query.get(user_id)
    reservation.leaving_timestamp = datetime.now()
    spot = ParkingSpot.query.get(reservation.spot_id)
    spot.status = 'A'
    if spot and spot.lot and hasattr(spot.lot, 'revenue'):
        revenue_earned = reservation.cost_per_hour * 1
        spot.lot.revenue += revenue_earned
    db.session.commit()
    flash("Spot released successfully.","success")
    return redirect(url_for("user_dashboard",user_id=user.id))

@app.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required(role=1)
def edit_user_profile(user_id):
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.pincode = request.form.get('pincode')
        user.address = request.form.get('address')
        db.session.commit()
        return redirect(url_for('user_dashboard', user_id=user.id))
    return render_template('user_edit_profile.html', user=user)

@app.route('/user/summary/<int:user_id>')
@login_required(role=1)
def user_summary(user_id):
    user = User.query.get_or_404(user_id)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    # --- Data ---
    total_spots = db.session.query(ParkingSpot).count()
    occupied_spots = db.session.query(ParkingSpot).filter_by(status='O').count()
    vacant_spots = total_spots - occupied_spots
    labels = ['Occupied', 'Vacant']
    values = [occupied_spots, vacant_spots]

    # --- Plotting ---
    plt.figure(figsize=(10, 7))  # Bigger figure
    bars = plt.bar(
        labels, 
        values, 
        color=['#FF4C4C', '#4CAF50'],  # Red & Green
        edgecolor='black',
        linewidth=1.5,
        alpha=0.85
    )

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height}",
            ha='center',
            va='bottom',
            fontsize=16,
            fontweight='bold',
            color='#333'
        )
    plt.ylabel('Number of Spots', fontsize=18, fontweight='bold')
    plt.xticks(fontsize=16, fontweight='bold')
    plt.yticks(fontsize=14)
    plt.ylim(0, max(values)*1.2)
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('static/user_parking_summary.png', transparent=True)
    plt.close()
    return render_template(
        'user_summary.html',
        total=total_spots,
        occupied=occupied_spots,
        vacant=vacant_spots,
        user=user
    )
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("signin"))

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/admin/mandirs')
@login_required(role=0)
def admin_mandirs():
    mandirs = Mandir.query.all()
    return render_template('admin_mandirs.html', mandirs=mandirs)

@app.route('/admin/mandir/add', methods=['GET', 'POST'])
@login_required(role=0)
def add_mandir():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        new_mandir = Mandir(name=name, address=address, pin_code=pin_code)
        db.session.add(new_mandir)
        db.session.commit()
        flash("Mandir added successfully!", "success")
        return redirect(url_for('admin_mandirs'))
    return render_template('add_mandir.html')

@app.route('/admin/mandir/<int:mandir_id>/delete', methods=['POST'])
@login_required(role=0)
def delete_mandir(mandir_id):
    mandir = Mandir.query.get_or_404(mandir_id)
    db.session.delete(mandir)
    db.session.commit()
    flash("Mandir deleted!", "success")
    return redirect(url_for('admin_mandirs'))

@app.route('/admin/slots')
@login_required(role=0)
def admin_slots():
    slots = DarshanSlot.query.order_by(DarshanSlot.start_time).all()
    return render_template('admin_slots.html', slots=slots)

@app.route('/admin/slot/add', methods=['GET','POST'])
@login_required(role=0)
def add_slot():
    if request.method == 'POST':
        slot_type = request.form.get('slot_type')
        start_time = datetime.strptime(request.form.get('start_time'), "%H:%M").time()
        end_time = datetime.strptime(request.form.get('end_time'), "%H:%M").time()
        max_visitors = int(request.form.get('max_visitors'))

        slot = DarshanSlot(
            mandir_id=1,   # since you only have 1 mandir
            slot_type=slot_type,
            start_time=start_time,
            end_time=end_time,
            max_visitors=max_visitors
        )
        db.session.add(slot)
        db.session.commit()
        flash("Slot added successfully!", "success")
        return redirect(url_for('admin_slots'))

    return render_template('add_slot.html')

@app.route('/admin/slot/edit/<int:slot_id>', methods=['GET','POST'])
@login_required(role=0)
def edit_slot(slot_id):
    slot = DarshanSlot.query.get_or_404(slot_id)

    if request.method == 'POST':
        slot.slot_type = request.form.get('slot_type')
        slot.start_time = datetime.strptime(request.form.get('start_time'), "%H:%M").time()
        slot.end_time = datetime.strptime(request.form.get('end_time'), "%H:%M").time()
        slot.max_visitors = int(request.form.get('max_visitors'))
        db.session.commit()
        flash("Slot updated successfully!", "success")
        return redirect(url_for('admin_slots'))

    return render_template('edit_slot.html', slot=slot)


@app.route('/admin/slot/delete/<int:slot_id>', methods=['POST'])
@login_required(role=0)
def delete_slot(slot_id):
    slot = DarshanSlot.query.get_or_404(slot_id)
    db.session.delete(slot)
    db.session.commit()
    flash("Slot deleted successfully!", "success")
    return redirect(url_for('admin_slots'))


@app.route('/user/book-ticket/<int:user_id>', methods=['GET', 'POST'])
@login_required(role=1)
def book_ticket(user_id):
    mandirs = Mandir.query.all()
    slots = DarshanSlot.query.order_by(DarshanSlot.start_time).all()
    lots = ParkingLot.query.all()
    user = User.query.get_or_404(user_id)
    
    QR_FOLDER = os.path.join("static", "qrcode")
    os.makedirs(QR_FOLDER, exist_ok=True)  # Ensure folder exists

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')
        slot_id = int(request.form.get('slot_id'))
        num_members = int(request.form.get('num_members'))
        parking_lot_id = request.form.get('parking_lot_id')
        passenger_names = request.form.getlist('passenger_name[]')
        vehicle_numbers = request.form.getlist('vehicle_numbers[]')
        aadhar_numbers = request.form.getlist('aadhar_number[]')
        entered_otps = request.form.getlist('otp[]')
        mobile_number = request.form.get('mobile_number')

        # --- Step 1: Slot capacity check ---
        slot = DarshanSlot.query.get(slot_id)
        current_booked = Ticket.query.filter_by(slot_id=slot.id).count()
        if current_booked + num_members > slot.max_visitors:
            flash(f"Cannot book {num_members} tickets. Only {slot.max_visitors - current_booked} slots left.", "danger")
            return redirect(url_for('book_ticket', user_id=user.id))

# Step 2: OTP Verification
        for i in range(num_members):
            aadhar = aadhar_numbers[i]
            otp_entered = entered_otps[i].strip()
            stored_otp = otp_storage.get(aadhar)

            if stored_otp != otp_entered:
                flash(f"OTP verification failed for {passenger_names[i]} (Aadhar {aadhar})", "danger")
                return redirect(url_for('book_ticket', user_id=user.id))

            # Remove OTP after successful verification
            otp_storage.pop(aadhar, None)       
            flash(f"OTP verified successfully for {passenger_names[i]}", "success")
        # --- Step 3: Ticket creation + QR + optional parking ---
        tickets = []

        for i in range(num_members):
            passenger_name = passenger_names[i] if i < len(passenger_names) else f"Guest{i+1}"

            # Create ticket first
            ticket = Ticket(user_id=user.id, slot_id=slot.id)
            db.session.add(ticket)
            db.session.commit()  # Now ticket.id is available

            # Generate QR code safely using ticket.id
            qr_data = str(ticket.id)  # or URL if needed
            qr_img = qrcode.make(qr_data)
            qr_filename = f"ticket_{ticket.id}_{secure_filename(passenger_name)}.png"
            qr_path = os.path.join(QR_FOLDER, qr_filename)
            qr_img.save(qr_path)

            ticket.qr_code = qr_filename
            db.session.commit()
            tickets.append(ticket)

            # --- Optional parking assignment ---
            if parking_lot_id and i < len(vehicle_numbers) and vehicle_numbers[i]:
                lot = ParkingLot.query.get(int(parking_lot_id))
                spot = next((s for s in lot.spots if s.status == 'A'), None)
                if spot:
                    spot.status = 'O'
                    reservation = Reservation(
                        spot_id=spot.id,
                        user_id=user.id,
                        vehicle_number=vehicle_numbers[i],
                        parking_timestamp=datetime.now(),
                        cost_per_hour=lot.price_per_hour
                    )
                    db.session.add(reservation)
                    db.session.commit()

                    ticket_parking = TicketParking(ticket_id=ticket.id, spot_id=spot.id, qr_code=qr_filename)
                    db.session.add(ticket_parking)
                    db.session.commit()


        for idx, ticket in enumerate(tickets):
            passenger_name = passenger_names[idx] if idx < len(passenger_names) else f"Guest{idx+1}"
            content_variables = f'{{"1":"{ticket.id}","2":"{slot.start_time.strftime("%Y-%m-%d %H:%M")}","3":"{passenger_name}"}}'
            try:
                TWILIO_CLIENT.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    content_sid=CONTENT_SID,
                    content_variables=content_variables,
                    to=f'whatsapp:{mobile_number}'
                )
            except Exception as e:
                flash(f"WhatsApp failed for ticket {ticket.id}: {e}", "danger")

        flash(f"{num_members} tickets booked successfully and sent to {mobile_number}!", "success")
        return render_template('ticket_confirmation.html', tickets=tickets, parking_lot_id=parking_lot_id,user=user)
        
    return render_template('admin_book_ticket.html', mandirs=mandirs, slots=slots, lots=lots, user=user)

@app.route('/send-otp', methods=['POST'])
@login_required(role=1)
def send_otp():
    """
    Sends OTP via WhatsApp for a given Aadhar number.
    """
    data = request.get_json()
    aadhar = data.get('aadhar')

    if not aadhar:
        return jsonify({"success": False, "message": "Aadhar missing"})

    mobile = AADHAR_MOBILE_MAP.get(aadhar)
    if not mobile:
        return jsonify({"success": False, "message": "Aadhar not registered"})

    otp = str(random.randint(100000, 999999))
    otp_storage[aadhar] = otp  # store OTP

    try:
        TWILIO_CLIENT.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=f"Your OTP for ticket booking is {otp}",
            to=f'whatsapp:{mobile}'
        )
        return jsonify({"success": True, "message": f"OTP sent to {mobile}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/admin/tickets')
@login_required(role=0)
def admin_tickets():
    tickets = Ticket.query.order_by(Ticket.id.desc()).all()
    return render_template('admin_tickets.html', tickets=tickets)

@app.route('/admin/ticket/<int:ticket_id>')
@login_required(role=0)
def admin_ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    parking = TicketParking.query.filter_by(ticket_id=ticket.id).first()
    return render_template('admin_ticket_detail.html', ticket=ticket, parking=parking)

# Folders
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/scan-ticket', methods=['GET', 'POST'])
@login_required(role=0)
def scan_ticket():
    ticket = None
    message = None

    if request.method == 'POST':
        # Check if user uploaded file
        file = request.files.get('qr_image')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            img = Image.open(filepath)
            decoded_objs = decode(img)
            if decoded_objs:
                qr_data = decoded_objs[0].data.decode('utf-8')
            else:
                qr_data = None
                flash("❌ Could not read QR code from uploaded file.", "danger")
        if qr_data:
            try:
                ticket_id = int(qr_data)
                ticket = Ticket.query.get_or_404(ticket_id)

                if ticket.scan_count == 0:
                    ticket.scan_count = 1
                    ticket.status = "Entered"
                    flash(f"✅ Entry granted for Ticket {ticket.id}", "success")
                elif ticket.scan_count == 1:
                    ticket.scan_count = 2
                    ticket.status = "Exited"
                    flash(f"✅ Exit recorded for Ticket {ticket.id}", "info")
                else:
                    flash(f"❌ Ticket {ticket.id} already expired.", "danger")
                db.session.commit()
            except ValueError:
                flash("❌ Invalid QR code content.", "danger")
    return render_template("scan_ticket.html", ticket=ticket)

@app.route('/scan-ticket-live', methods=['POST'])
@login_required(role=0)
def scan_ticket_live():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    try:
        ticket_id = int(ticket_id)
        ticket = Ticket.query.get_or_404(ticket_id)

        if ticket.scan_count == 0:
            ticket.scan_count = 1
            ticket.status = "Entered"
            message = f"✅ Entry granted for Ticket {ticket.id}"
            status = "success"
        elif ticket.scan_count == 1:
            ticket.scan_count = 2
            ticket.status = "Exited"
            message = f"✅ Exit recorded for Ticket {ticket.id}"
            status = "success"
        else:
            message = f"❌ Ticket {ticket.id} already expired."
            status = "error"

        db.session.commit()
        return jsonify({"success": True, "message": message, "status": status})
    except Exception as e:
        return jsonify({"success": False, "message": f"❌ Invalid QR: {e}", "status": "error"})

@app.route('/calendar_user/<int:user_id>')
def calendar_user(user_id):
    user=User.query.get_or_404(user_id)
    return render_template('calendar_page2.html',user=user)

@app.route('/calendar')
def calendar_admin():
    return render_template('calendar_page.html')

@app.route('/verify-otp', methods=['POST'])
@login_required(role=1)
def verify_otp():
    """
    Verify OTP sent for Aadhar number.
    This route is called from front-end via AJAX when user enters OTP.
    The OTP is NOT removed from otp_storage here, so booking can succeed later.
    """
    data = request.get_json()
    aadhar = data.get('aadhar')
    otp_entered = data.get('otp', '').strip()  # trim extra spaces

    if not aadhar or not otp_entered:
        return jsonify({"success": False, "message": "Aadhar or OTP missing"})

    stored_otp = otp_storage.get(aadhar)
    if stored_otp == otp_entered:
        # OTP verified successfully but we don't pop it yet
        return jsonify({"success": True, "message": "OTP Verified"})
    else:
        return jsonify({"success": False, "message": "OTP Invalid"})
