from flask_restplus import Namespace, Resource, fields, abort
from api import api, db
from flask import request
from models.seat import SeatModel
from session import require_session

seat_api = Namespace('seat')

requestSchema = {
    "CreateSeatModel": api.model("create seat", {
        "room": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of room"),
        "block": fields.Integer(required=True),
        "row": fields.Integer(required=True),
        "accessible": fields.Boolean(required=True),
    }),
    "SpecificSeatModel": api.model("specific seat", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of seat"),
    }),
    "AllSeatModel": api.model("all seats of room", {
        "room": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of room"),
    }),
}

responseSchema = {
    "SeatModel": api.model("seat", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of seat"),
        "room": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of room"),
        "block": fields.Integer(required=True),
        "row": fields.Integer(required=True),
        "column": fields.Integer(required=True),
        "accessible": fields.Boolean(required=True),
    }),
    "SuccessModel": api.model("success", {
        "result": fields.Boolean(required=True)
    })
}

@seat_api.route('/')
@seat_api.doc('general seat actions')
class GeneralSeatService(Resource):

    @seat_api.doc('create a seat')
    @seat_api.expect(requestSchema["CreateSeatModel"])
    @seat_api.marshal_with(responseSchema["SeatModel"])
    @require_session
    def put(self, session):
        room = request.json["room"]
        block = request.json["block"]
        row = request.json["row"]
        accessible = request.json["accessible"]

        seat: SeatModel = SeatModel.create(room, block, row, accessible)

        return seat.serialize

    @seat_api.doc('get all seats')
    def get(self):
        seats: list = SeatModel.query.all()

        return {'seats': [s.serialize for s in seats]}

    @seat_api.doc('get all seats of room')
    @seat_api.expect(requestSchema["AllSeatModel"])
    @require_session
    def post(self, session):
        uuid = request.json["room"]

        seats: list = SeatModel.query.filter_by(room_id=uuid).all()

        return {'seats': [s.serialize for s in seats]}


@seat_api.route('/<string:uuid>')
@seat_api.doc('specific seat actions')
class SpecificSeatService(Resource):

    @seat_api.doc('get a seat')
    @seat_api.expect(requestSchema["SpecificSeatModel"])
    @seat_api.marshal_with(responseSchema["SuccessModel"])
    @seat_api.response(404, "Not Found", {})
    def get(self, uuid):
        seat: SeatModel = SeatModel.query.filter_by(uuid=uuid).first()

        return seat.serialize

    @seat_api.doc('delete a seat')
    @seat_api.expect(requestSchema["SpecificSeatModel"])
    @seat_api.marshal_with(responseSchema["SuccessModel"])
    @seat_api.response(404, "Not Found", {})
    @require_session
    def delete(self, uuid, session):
        seat: SeatModel = SeatModel.query.filter_by(uuid=uuid).first()

        db.session.delete(seat)
        db.session.commit()

        return True