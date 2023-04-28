from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'team16'
    app.instance_path = Path(".").resolve()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
