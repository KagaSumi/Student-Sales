from os import path
from flask import Flask
from pathlib import Path
from database.database import db
from flask_login import LoginManager
from database.models import User,Listing

DB_NAME = "database.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'team16'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///database/{DB_NAME}'
app.instance_path = Path(".").resolve()

db.init_app(app)

from routes.auth import auth
app.register_blueprint(auth, url_prefix='/')

from routes.views import views
app.register_blueprint(views, url_prefix='/')

if not path.exists(f'database/{DB_NAME}'):
    with app.app_context():
        db.create_all()
        print('Database Created!')

if __name__ == '__main__':
    app.run(debug=True)
