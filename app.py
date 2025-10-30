import os
from flask import Flask
from models.model import db
app=None
def setup_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///DevDhamPath.sqlite3"
    db.init_app(app)
    app.app_context().push()
    app.debug=True
    print("DevDhamPath App Started")
    app.secret_key = os.urandom(24)  
app=setup_app()##why  do we do this? .... to avoid circular import
if not os.path.exists("instance/DevDhamPath.sqlite3"):
    db.create_all()
    print("Database Created")
    from create_initial_data import *
from controllers.controller import *
if __name__=="__main__":
    app.run(debug=True)