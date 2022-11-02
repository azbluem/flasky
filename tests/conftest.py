import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.breakfasts import Breakfast


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_breakfasts(app):
    brek1 = Breakfast(
        name = "Cheese Omelet",
        rating = 4.0,
        prep_time = 25
    )
    brek2 = Breakfast(
        name = "Continental",
        rating = 2.5,
        prep_time = 0
    )

    db.session.add(brek1,brek2)
    db.session.commit()