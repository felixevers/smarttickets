from flask_restplus import Namespace, Resource, fields, abort
from api import api
from flask import request
from models.setting import SettingModel

setting_api = Namespace('setting')

requestSchema = {
    "SettingUpdateService": api.model("update a setting", {
        "key": fields.String(required=True, example="color",
                             description="key of setting"),
        "value": fields.String(required=True, example="blue",
                               description="value of setting")
    })
}

responseSchema = {
}


# TODO require a session of an administrator
@setting_api.route('/')
@setting_api.doc('set setting')
class SettingService(Resource):

    @setting_api.doc('update a setting')
    @setting_api.expect(requestSchema["SettingUpdateService"])
    def post(self):
        key = request.json["key"]
        value = request.json["value"]

        setting: SettingModel = SettingModel.query.filter_by(key=key).first()

        if setting:
            setting.value = value
            return setting.serialize
        else:
            return 400

    @setting_api.doc('create a setting')
    @setting_api.expect(requestSchema["SettingUpdateService"])
    def put(self):
        key = request.json["key"]
        value = request.json["value"]

        setting: SettingModel = SettingModel.query.filter_by(key=key).first()

        if setting:
            return 400
        else:
            setting: SettingModel = SettingModel.create(key, value)
            return setting.serialize
