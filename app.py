import json, sys
from os import path
from flask import Flask
from pathlib import Path
from routes.user import user
from routes.auth import auth
from routes.views import views
from routes.message import message
from database.database import db
from routes.listing import listing
from flask_login import LoginManager
from database.models import User, Listing
from routes.public_view import public_view
from routes.private_view import private_view
from extensions import mail

DB_NAME = "database.db"

# Flask Server Setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "team16"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database/{DB_NAME}"
app.instance_path = Path(".").resolve()

# Register Sqlalchemy With Flask Instance
db.init_app(app)

#Mail Service
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@flask.com'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = False
app.config['MAIL_USERNAME'] = 'studentsales.bcit@gmail.com' # This account will be deactivated after our project is shown but is just a gmail address
app.config['MAIL_PASSWORD'] = 'nqnqyiolbycbxmlh'

# Register Route Blueprints
app.register_blueprint(user, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(views, url_prefix="/")
app.register_blueprint(listing, url_prefix="/")
app.register_blueprint(public_view, url_prefix="/")
app.register_blueprint(private_view, url_prefix="/")
app.register_blueprint(message, url_prefix="/")

# Create Database File
if not path.exists(f"database/{DB_NAME}"):
    with app.app_context():
        db.create_all()
        print("Database Created!")

# Flask Login Setup
login_manager = LoginManager()
login_manager.login_view = "public_view.login"
login_manager.login_message = "You Must Login to Access This Page!"
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Custom Jinja Filters
@app.template_filter('from_json')
def from_json_filter(value):
    return json.loads(value)

if __name__ == "__main__":
    def main(password:str,host:str =None,port:int =None):
        app.config['MAIL_PASSWORD'] = password
        mail.init_app(app)
        if host is None and port is None: 
            app.run(debug=True)
        else:
            app.run(host=host,port=port)
    args = sys.argv[1:]
    if len(args) == 1 or len(args) == 3:
        main(*args)
    elif len(args) == 2 or len(args) == 0:
        output ="""
    Starts the application with the provided password, host, and port.

    Args:
        password (str): The password for the mail configuration.
        host (str, optional): The host IP address to bind the application to. Defaults to None.
        port (int, optional): The port number to bind the application to. Defaults to None.
    """
        print(output)