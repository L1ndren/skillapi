from datetime import datetime

from flask import jsonify, request

from .extensions import db
from .models import Client, ClientParking, Parking


def init_routes(app):
    @app.route("/clients", methods=["GET"])
    def get_clients():
        clients = Client.query.all()
        return jsonify([client.to_dict() for client in clients])

    # ... (остальные маршруты без изменений)

    @app.route("/client_parkings", methods=["DELETE"])
    def exit_parking():
        data = request.get_json()
        client_id = data["client_id"]
        parking_id = data["parking_id"]

        client = Client.query.get_or_404(client_id)
        parking = Parking.query.get_or_404(parking_id)

        if not client.credit_card:
            return (
                jsonify({"error": "Client has no credit card"}),
                400,
            )  # Разбито на 2 строки

        client_parking = ClientParking.query.filter_by(
            client_id=client_id, parking_id=parking_id, time_out=None
        ).first_or_404()

        client_parking.time_out = datetime.utcnow()
        parking.count_available_places += 1
        db.session.commit()

        return jsonify(client_parking.to_dict()), 200
