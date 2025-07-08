import pytest
from .factories import ClientFactory, ParkingFactory
from ..models import Parking


@pytest.mark.usefixtures('app')
def test_client_factory(db_session):
    client = ClientFactory()
    assert client.name is not None
    assert client.surname is not None
    assert isinstance(client.name, str)
    assert isinstance(client.surname, str)


@pytest.mark.usefixtures('app')
def test_parking_factory(db_session):
    parking = ParkingFactory(opened=True)
    assert parking.address is not None
    assert parking.count_places > 0
    assert parking.count_available_places == parking.count_places

    closed_parking = ParkingFactory(opened=False)
    assert closed_parking.count_available_places == 0