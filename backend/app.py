import os
from flask import Flask, jsonify
from flask_cors import CORS
from models.model import db
from controller import api

def create_app():
    """Initialize and configure the Flask application."""
    app = Flask(__name__)

    # Configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DevDhamPath.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.urandom(24)
    app.debug = True

    # Initialize extensions
    CORS(app)
    db.init_app(app)

    # Register blueprints / controllers
    api.init_app(app)

    @app.route("/api/hello")
    def hello():
        return jsonify({"message": "Hello from Flask!!!!"})

    return app


# Create the Flask application
app = create_app()

# Create database if it doesn't exist
db_path = os.path.join("instance", "DevDhamPath.sqlite3")
if not os.path.exists(db_path):
    with app.app_context():
        db.create_all()
        print("✅ Database Created")
        from create_initial_data import *


if __name__ == "__main__":
    print("🚀 DevDhamPath App Started")
    app.run(debug=True)
