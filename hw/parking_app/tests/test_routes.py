import pytest
from datetime import datetime
from ..models import Parking


@pytest.mark.parametrize('url', ['/clients', '/clients/1'])
def test_get_methods(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client):
    data = {
        'name': 'New',
        'surname': 'Client',
        'credit_card': '9876543210987654',
        'car_number': 'X999XX'
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    assert 'id' in response.json


def test_create_parking(client):
    data = {
        'address': 'New Parking',
        'count_places': 20
    }
    response = client.post('/parkings', json=data)
    assert response.status_code == 201
    assert response.json['count_available_places'] == 20


@pytest.mark.parking
def test_enter_closed_parking(client, db_session):
    data = {'client_id': 1, 'parking_id': 2}
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400
    assert response.json == {'error': 'Parking is closed'}


@pytest.mark.parking
def test_enter_full_parking(client, db_session):
    data = {'client_id': 1, 'parking_id': 3}
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400
    assert response.json == {'error': 'No available places'}


def test_exit_parking(client, db_session):
    # First enter parking
    enter_data = {'client_id': 1, 'parking_id': 1}
    client.post('/client_parkings', json=enter_data)

    # Then exit
    response = client.delete('/client_parkings', json=enter_data)
    assert response.status_code == 200
    assert 'time_out' in response.json
