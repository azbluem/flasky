from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(testing = None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    CORS(app)
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
    from app.models.menu import Menu
    from app.models.ingredients import Ingredients

    from .routes.breakfast import breakfast_bp
    app.register_blueprint(breakfast_bp)

    from .routes.menu import menu_bp
    app.register_blueprint(menu_bp)

    # from .routes.ingredients import ingredient_bp
    # app.register_blueprint(ingredient_bp)

    return app