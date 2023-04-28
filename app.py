from os import path
from flask import Flask
from pathlib import Path
from database.database import db
from flask_login import LoginManager
from database.models import User,Listing

DB_NAME = "database.db"

# Flask Server Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'team16'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database/{DB_NAME}'
app.instance_path = Path(".").resolve()

# Assign Sqlalchemy Flask Instance
db.init_app(app)

# Register Route Blueprints
from routes.auth import auth
app.register_blueprint(auth, url_prefix='/')

from routes.views import views
app.register_blueprint(views, url_prefix='/')

# Create Database File
if not path.exists(f'database/{DB_NAME}'):
    with app.app_context():
        db.create_all()
        print('Database Created!')

# Flask Login Setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'You Must Login to Access This Page!'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    app.run(debug=True)
