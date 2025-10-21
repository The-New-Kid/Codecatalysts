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
setup_app()
from controllers.controller import *
if __name__=="__main__":
    app.run(debug=True)