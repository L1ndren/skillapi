import pytest
from datetime import datetime, timezone
from ..models import Parking

@pytest.mark.parametrize('url', [
    '/clients',
    '/clients/1',
])
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
    # Получаем закрытую парковку из базы
    closed_parking = db_session.get(Parking, 2)
    assert not closed_parking.opened  # Проверяем что она действительно закрыта

    data = {
        'client_id': 1,
        'parking_id': 2
    }
    response = client.post('/client_parkings', json=data)

    # Ожидаем 400 и проверяем сообщение об ошибке
    assert response.status_code == 400
    assert response.json == {'error': 'Parking is closed'}


@pytest.mark.parking
def test_enter_full_parking(client, db_session):
    # Получаем полную парковку из базы
    full_parking = db_session.get(Parking, 3)
    assert full_parking.count_available_places == 0  # Проверяем что она действительно полная

    data = {
        'client_id': 1,
        'parking_id': 3
    }
    response = client.post('/client_parkings', json=data)

    # Ожидаем 400 и проверяем сообщение об ошибке
    assert response.status_code == 400
    assert response.json == {'error': 'No available places'}

@pytest.mark.parking
def test_exit_parking(client, db_session):
    from ..models import Parking
    # Сначала создаем запись о въезде
    data = {
        'client_id': 1,
        'parking_id': 1
    }
    client.post('/client_parkings', json=data)

    # Теперь выезжаем
    response = client.delete('/client_parkings', json=data)
    assert response.status_code == 200
    assert 'time_out' in response.json

    # Проверка через сессию БД
    parking = db_session.get(Parking, 1)
    assert parking.count_available_places == 10


@pytest.mark.parking
def test_enter_closed_parking(client):
    data = {
        'client_id': 1,
        'parking_id': 2  # Закрытая парковка (ID=2)
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400
    assert 'error' in response.json


@pytest.mark.parking
def test_enter_full_parking(client):
    data = {
        'client_id': 1,
        'parking_id': 3  # Полная парковка (ID=3)
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 400
    assert 'error' in response.json