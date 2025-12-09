import os
from flask import Flask, jsonify
from flask_cors import CORS
from models.model import db, Aarti_and_DarshanSlot
from controller import api
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import requests
import atexit

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DevDhamPath.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.urandom(24)
    app.debug = True

    # Initialize extensions
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)

    api.init_app(app)

    @app.route("/api/hello")
    def hello():
        return jsonify({"message": "Hello from Flask!!!!"})

    return app


app = create_app()


# ================== SCHEDULER SYSTEM =================== #

scheduler = BackgroundScheduler()

def schedule_subslot_reminders():
    """Schedules notification jobs 30 mins before each slot start today"""
    with app.app_context():
        today = datetime.now().date()
        slots = Aarti_and_DarshanSlot.query.all()

        for slot in slots:
            slot_start = datetime.combine(today, slot.start_time)
            notify_time = slot_start - timedelta(minutes=10)

            # We only schedule future jobs
            if notify_time > datetime.now():
                job_id = f"slot_{slot.id}_{today}"

                scheduler.add_job(
                    func=lambda: trigger_subslot_reminder(slot.id),
                    trigger='date',
                    run_date=notify_time,
                    id=job_id,
                    replace_existing=True
                )

                print(f"⏳ Scheduled reminder for slot {slot.slot_type} at {notify_time.time()}")


def trigger_subslot_reminder(slot_id):
    """Called exactly 30 mins before a specific slot"""
    print(f"🔔 Triggering reminders for slot {slot_id} at", datetime.now())

    try:
        requests.post("http://localhost:5000/api/allocate-subslots", timeout=10)
    except Exception as e:
        print("Reminder trigger failed:", e)


# Start scheduler only once (avoid double starts in debug mode)
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    schedule_subslot_reminders()
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    print("🛕 Scheduler Started (Smart Mode)")


# ==================== Database Create ==================== #

db_path = os.path.join("instance", "DevDhamPath.sqlite3")
if not os.path.exists(db_path):
    with app.app_context():
        db.create_all()
        print("🧱 Database Created")
        from create_initial_data import *


if __name__ == "__main__":
    print("🚀 DevDhamPath App Started")
    app.run(host="0.0.0.0", port=5000, debug=True)
