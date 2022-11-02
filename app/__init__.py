from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(testing = None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if not testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_ECHO'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_TEST_URI')
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True

    db.init_app(app)
    migrate.init_app(app,db)

    from app.models.breakfasts import Breakfast

    from .routes.breakfast import breakfast_bp
    app.register_blueprint(breakfast_bp)

    return app