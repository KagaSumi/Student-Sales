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

DB_NAME = "database.db"

# Flask Server Setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "team16"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database/{DB_NAME}"
app.instance_path = Path(".").resolve()

# Register Sqlalchemy With Flask Instance
db.init_app(app)

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
login_manager.login_view = "public_view.login"
login_manager.login_message = "You Must Login to Access This Page!"
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == "__main__":
    app.run(debug=True)
