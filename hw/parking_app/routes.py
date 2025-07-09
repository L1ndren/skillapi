from flask import request, jsonify
from datetime import datetime
from .extensions import db
from .models import Client, Parking, ClientParking


def init_routes(app):
    @app.route('/clients', methods=['GET', 'POST'])
    def handle_clients():
        if request.method == 'GET':
            clients = Client.query.all()
            return jsonify([client.to_dict() for client in clients])
        elif request.method == 'POST':
            data = request.get_json()
            client = Client(
                name=data['name'],
                surname=data['surname'],
                credit_card=data.get('credit_card'),
                car_number=data.get('car_number')
            )
            db.session.add(client)
            db.session.commit()
            return jsonify(client.to_dict()), 201

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        client = Client.query.get_or_404(client_id)
        return jsonify(client.to_dict())

    @app.route('/parkings', methods=['POST'])
    def create_parking():
        data = request.get_json()
        parking = Parking(
            address=data['address'],
            opened=data.get('opened', True),
            count_places=data['count_places'],
            count_available_places=data['count_places']
        )
        db.session.add(parking)
        db.session.commit()
        return jsonify(parking.to_dict()), 201

    @app.route('/client_parkings', methods=['POST', 'DELETE'])
    def handle_client_parkings():
        if request.method == 'POST':
            data = request.get_json()
            client_id = data['client_id']
            parking_id = data['parking_id']

            parking = Parking.query.get_or_404(parking_id)

            if not parking.opened:
                return jsonify({'error': 'Parking is closed'}), 400

            if parking.count_available_places <= 0:
                return jsonify({'error': 'No available places'}), 400

            client_parking = ClientParking(
                client_id=client_id,
                parking_id=parking_id,
                time_in=datetime.utcnow()
            )

            parking.count_available_places -= 1
            db.session.add(client_parking)
            db.session.commit()

            return jsonify(client_parking.to_dict()), 201

        elif request.method == 'DELETE':
            data = request.get_json()
            client_id = data['client_id']
            parking_id = data['parking_id']

            parking = Parking.query.get_or_404(parking_id)

            client_parking = ClientParking.query.filter_by(
                client_id=client_id,
                parking_id=parking_id,
                time_out=None
            ).first_or_404()

            client_parking.time_out = datetime.utcnow()
            parking.count_available_places += 1
            db.session.commit()

            return jsonify(client_parking.to_dict()), 200
