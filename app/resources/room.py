from flask_restplus import Namespace, Resource, fields, abort
from api import api, db
from flask import request
from models.room import RoomModel
from session import require_session

room_api = Namespace('room')

requestSchema = {
    "CreateRoomModel": api.model("create room", {
        "name": fields.String(required=True, example="Hall01",
                              description="name of room"),
    }),
    "SpecificRoomModel": api.model("specific room", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of room"),
    })
}

responseSchema = {
    "RoomModel": api.model("room", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of room"),
        "name": fields.String(required=True, example="Hall01",
                              description="name of room"),
    }),
    "SuccessModel": api.model("success", {
        "result": fields.Boolean(required=True)
    })
}

@room_api.route('/')
@room_api.doc('general room actions')
class GeneralRoomService(Resource):

    @room_api.doc('create a room')
    @room_api.expect(requestSchema["CreateRoomModel"])
    @room_api.marshal_with(responseSchema["RoomModel"])
    @require_session
    def put(self, session):
        name = request.json["name"]

        room: RoomModel = RoomModel.create(name)

        return room.serialize

    @room_api.doc('get all rooms')
    def get(self):
        rooms: list = RoomModel.query.all()

        return [r.serialize for r in rooms]


@room_api.route('/<string:uuid>')
@room_api.doc('specific room actions')
class SpecificRoomService(Resource):

    @room_api.doc('get a room')
    @room_api.expect(requestSchema["SpecificRoomModel"])
    @room_api.marshal_with(responseSchema["SuccessModel"])
    @room_api.response(404, "Not Found", {})
    def get(self, uuid):
        room: RoomModel = RoomModel.query.filter_by(uuid=uuid).first()

        return room.serialize

    @room_api.doc('delete a room')
    @room_api.expect(requestSchema["SpecificRoomModel"])
    @room_api.marshal_with(responseSchema["SuccessModel"])
    @room_api.response(404, "Not Found", {})
    @require_session
    def delete(self, uuid, session):
        room: RoomModel = RoomModel.query.filter_by(uuid=uuid).first()

        db.session.delete(room)
        db.session.commit()

        return True
