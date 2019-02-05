from flask_restplus import Namespace, Resource, fields, abort
from api import api
from flask import request
from models.meeting import MeetingModel

meeting_api = Namespace('meeting')

requestSchema = {
    "MeetingCreateModel": api.model("create a meeting", {
        "name": fields.String(required=True, example="Hairspray",
                              description="name of meeting"),
        "description": fields.String(required=True, example="A musical written by...",
                                     description="short description of the meeting")
    }),
    "MeetingGetAllModel": api.model("get all meetings", {
    }),
    "MeetingGetModel": api.model("get specific meeting", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="name of meeting")
    })
}

responseSchema = {
    "MeetingModel": api.model("meeting", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of meeting"),
        "name": fields.String(required=True, example="Hairspray",
                              description="name of meeting"),
        "description": fields.String(required=True, example="A musical written by...",
                                     description="short description of the meeting"),
    }),
    "MeetingModelList": api.model("array of all meetings", {
        "meetings": fields.List(fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of meeting"), description="list of all meetings")
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

        print(result)

        return {
            "meetings": result
        }

    @meeting_api.doc('create a meeting')
    @meeting_api.expect(requestSchema["MeetingCreateModel"])
    @meeting_api.marshal_with(responseSchema["MeetingModel"])
    def put(self):
        name = request.json["name"]
        description = request.json["description"]

        meeting: MeetingModel = MeetingModel.create(name, description)

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
