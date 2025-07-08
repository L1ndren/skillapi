import factory
from factory import alchemy
from faker import Faker

from ..extensions import db
from ..models import Client, Parking

fake = Faker()


class ClientFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyAttribute(
        lambda x: fake.credit_card_number() if fake.boolean() else None
    )
    car_number = factory.LazyAttribute(
        lambda x: (
            f"{fake.random_uppercase_letter()}"
            f"{fake.random_int(min=100, max=999)}"
            f"{fake.random_uppercase_letter()}"
            f"{fake.random_uppercase_letter()}"
        )
    )


class ParkingFactory(alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    address = factory.Faker("street_address")
    opened = factory.Faker("boolean")
    count_places = factory.Faker("random_int", min=1, max=100)
    count_available_places = factory.LazyAttribute(
        lambda o: o.count_places if o.opened else 0
    )
