from flask_restplus import Namespace, Resource, fields, abort
from api import api, db
from flask import request
from models.setting import SettingModel
from session import require_session

setting_api = Namespace('setting')

requestSchema = {
    "SettingUpdateService": api.model("update a setting", {
        "key": fields.String(required=True, example="color",
                             description="key of setting"),
        "value": fields.String(required=True, example="blue",
                               description="value of setting")
    }),
    "GetSettingService": api.model("get a setting", {
        "key": fields.String(required=True, example="color",
                             description="key of setting")
    })
}

responseSchema = {
}


@setting_api.route('/<string:key>')
@setting_api.doc('get setting')
class GetSettingService(Resource):

    @setting_api.doc('get a setting')
    @setting_api.expect(requestSchema["GetSettingService"])
    def get(self, key):
        setting: SettingModel = SettingModel.query.filter_by(key=key).first()

        if setting:
            return setting.serialize
        else:
            return { "key": key, "value": "" }

# TODO require a session of an administrator
@setting_api.route('/')
@setting_api.doc('set setting')
class SettingService(Resource):

    @setting_api.doc('update a setting')
    @setting_api.expect(requestSchema["SettingUpdateService"])
    @require_session
    def post(self, session):
        key = request.json["key"]
        value = request.json["value"]

        setting: SettingModel = SettingModel.query.filter_by(key=key).first()

        if setting:
            setting.value = value

            db.session.commit()

            return setting.serialize
        else:
            return { "result": False }

    @setting_api.doc('create a setting')
    @setting_api.expect(requestSchema["SettingUpdateService"])
    @require_session
    def put(self, session):
        key = request.json["key"]
        value = request.json["value"]

        setting: SettingModel = SettingModel.query.filter_by(key=key).first()

        if setting:
            return { "result": False }
        else:
            setting: SettingModel = SettingModel.create(key, value)
            return setting.serialize
