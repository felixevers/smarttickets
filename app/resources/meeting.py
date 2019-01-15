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
    "MeetingModelList": api.model("array of meetings", {
        "list": fields.List(cls_or_instance="", required=True, example="", description="list of all meetings")
    })
}


# TODO require a session of an administrator
@meeting_api.route('/')
@meeting_api.doc('create meeting')
class MeetingCreateService(Resource):

    @meeting_api.doc('get all meetingd')
    @meeting_api.expect(requestSchema["MeetingGetAllModel"])
    @meeting_api.marshal_with(responseSchema["MeetingModelList"])
    def get(self):
        return None

    @meeting_api.doc('create a meeting')
    @meeting_api.expect(requestSchema["MeetingCreateModel"])
    @meeting_api.marshal_with(responseSchema["MeetingModel"])
    def post(self):
        name = request.json["name"]
        description = request.json["description"]

        meeting: MeetingModel = MeetingModel.create(name, description)

        return meeting.serialize
