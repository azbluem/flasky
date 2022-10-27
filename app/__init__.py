from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/breakfasts_dev'
    
    db.init_app(app)
    migrate.init_app(app,db)

    from app.models.breakfasts import Breakfast

    from .routes.breakfast import breakfast_bp
    app.register_blueprint(breakfast_bp)

    return app