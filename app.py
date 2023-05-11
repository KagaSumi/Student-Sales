from os import path
from flask import Flask
from pathlib import Path
from routes.user import user
from routes.auth import auth
from routes.views import views
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
app.config['MAIL_USERNAME'] = 'studentsales.bcit@gmail.com' #This account will be deactivated after our project is shown but is just a gmail addr
app.config['MAIL_PASSWORD'] = 'nqnqyiolbycbxmlh'
app.config['SECRET_KEY'] = 'fdkjshfhjsdfdskfdsfdcbsjdkfdsdf'
mail.init_app(app)
# Register Route Blueprints
app.register_blueprint(user, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(views, url_prefix="/")
app.register_blueprint(listing, url_prefix="/")
app.register_blueprint(public_view, url_prefix="/")
app.register_blueprint(private_view, url_prefix="/")

# Create Database File
if not path.exists(f"database/{DB_NAME}"):
    with app.app_context():
        db.create_all()
        print("Database Created!")

# Flask Login Setup
login_manager = LoginManager()
login_manager.login_view = "auth.user_login"
login_manager.login_message = "You Must Login to Access This Page!"
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == "__main__":
    app.run(debug=True)
