import pytest

from ..app import create_app
from ..extensions import db
from ..models import Client, Parking


@pytest.fixture
def app():
    app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                      "TESTING": True})

    with app.app_context():
        db.create_all()

        client = Client(
            name="Test",
            surname="User",
            credit_card="1234567890123456",
            car_number="A123BC",
        )
        db.session.add(client)

        parking = Parking(
            id=1,
            address="Test Street, 1",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        db.session.add(parking)

        closed_parking = Parking(
            id=2,
            address="Closed Street, 1",
            opened=False,
            count_places=5,
            count_available_places=5,
        )
        db.session.add(closed_parking)

        full_parking = Parking(
            id=3,
            address="Full Street, 1",
            opened=True,
            count_places=1,
            count_available_places=0,
        )
        db.session.add(full_parking)

        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
