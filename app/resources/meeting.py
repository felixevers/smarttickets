from flask_restplus import Namespace, Resource, fields, abort
from api import api, db
from flask import request
from models.meeting import MeetingModel
from models.room import RoomModel
from models.price import PriceModel
from datetime import datetime
from session import require_session

meeting_api = Namespace('meeting')

requestSchema = {
    "MeetingCreateModel": api.model("create a meeting", {
        "name": fields.String(required=True, example="Hairspray",
                              description="name of meeting"),
        "description": fields.String(required=True, example="A musical written by...",
                                     description="short description of the meeting"),
        "room": fields.String(required=True),
        "date": fields.Integer(required=True),
        "start": fields.Integer(required=True),
        "stop": fields.Integer(required=True),
    }),
    "MeetingGetAllModel": api.model("get all meetings", {
    }),
    "MeetingGetModel": api.model("get specific meeting", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="name of meeting")
    }),
    "MeetingUpdateModel": api.model("create a meeting", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="name of meeting"),
        "name": fields.String(required=True, example="Hairspray",
                              description="name of meeting"),
        "description": fields.String(required=True, example="A musical written by...",
                                     description="short description of the meeting"),
        "room": fields.String(required=True),
        "date": fields.Integer(required=True),
        "start": fields.Integer(required=True),
        "stop": fields.Integer(required=True),
    }),
}

responseSchema = {
    "MeetingModel": api.model("meeting", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of meeting"),
        "name": fields.String(required=True, example="Hairspray",
                              description="name of meeting"),
        "description": fields.String(required=True, example="A musical written by...",
                                     description="short description of the meeting"),
        "room": fields.String(required=True),
        "date": fields.Integer(required=True),
        "start": fields.Integer(required=True),
        "stop": fields.Integer(required=True),
    }),
    "MeetingModelList": api.model("array of all meetings", {
        "meetings": fields.List(fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of meeting"), description="list of all meetings")
    }),
    "SuccessSchema": api.model("success", {
        "result": fields.Boolean(required=True)
    })
}

# TODO require a session of an administrator
@meeting_api.route('/')
@meeting_api.doc('general meeting actions')
class GeneralMeetingService(Resource):

    @meeting_api.doc('get all meetings')
    @meeting_api.expect(requestSchema["MeetingGetAllModel"])
    @meeting_api.marshal_with(responseSchema["MeetingModelList"])
    def get(self):
        result: list = []

        meetings: list = MeetingModel.query.all()

        for meeting in meetings:
            result.append(meeting.uuid)

        return {
            "meetings": result
        }

    @meeting_api.doc('create a meeting')
    @meeting_api.expect(requestSchema["MeetingCreateModel"])
    @meeting_api.marshal_with(responseSchema["MeetingModel"])
    @require_session
    def put(self, session):
        name = request.json["name"]
        description = request.json["description"]
        room_uuid = request.json["room"]
        date = request.json["date"]
        start = request.json["start"]
        stop = request.json["stop"]

        room: RoomModel = RoomModel.query.filter_by(uuid=room_uuid).first()

        meeting: MeetingModel = MeetingModel.create(name, description, room.uuid, date, start, stop)

        return meeting.serialize


@meeting_api.route('/<string:uuid>')
@meeting_api.doc('specific meeting actions')
class SpecificMeetingService(Resource):

    @meeting_api.doc('returns general information about the meeting')
    @meeting_api.expect(requestSchema["MeetingGetModel"])
    @meeting_api.marshal_with(responseSchema["MeetingModel"])
    @meeting_api.response(404, "Not Found", {})
    def get(self, uuid: str):
        meeting = MeetingModel.query.filter_by(uuid=uuid).first()

        return meeting.serialize

    @meeting_api.doc('deletes a meeting')
    @meeting_api.expect(requestSchema["MeetingGetModel"])
    @meeting_api.marshal_with(responseSchema["MeetingModel"])
    @meeting_api.response(404, "Not Found", {})
    @require_session
    def delete(self, uuid: str, session):
        meeting = MeetingModel.query.filter_by(uuid=uuid).first()

        db.session.delete(meeting)
        db.session.commit()

        return True

    @meeting_api.doc('update a meeting')
    @meeting_api.expect(requestSchema["MeetingUpdateModel"])
    @meeting_api.marshal_with(responseSchema["MeetingModel"])
    @meeting_api.response(404, "Not Found", {})
    @require_session
    def post(self, uuid: str, session):
        name = request.json["name"]
        description = request.json["description"]
        room_uuid = request.json["room"]
        date = request.json["date"]
        start = request.json["start"]
        stop = request.json["stop"]

        meeting = MeetingModel.query.filter_by(uuid=uuid).first()

        meeting.name = name
        meeting.description = description
        meeting.room = RoomModel.query.filter_by(uuid=room_uuid).first().uuid
        meeting.date = date
        meeting.start = start
        meeting.stop = stop

        db.session.commit()

        return True
