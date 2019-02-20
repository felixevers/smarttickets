from flask_restplus import Namespace, Resource, fields, abort
from api import api, db
from sqlalchemy import func
from flask import request
from flask_bcrypt import check_password_hash, generate_password_hash
from models.administrator import AdministratorModel
from models.session import SessionModel
from session import require_session
from flask import jsonify

administrator_api = Namespace('administrator')

requestSchema = {
    "AdministratorModel": api.model('administrator with password', {
        "firstname": fields.String(required=True, example="Max", description="firstname"),
        "lastname": fields.String(required=True, example="Mustermann", description="lastname"),
        "password": fields.String(required=True, example="qwertz", description="password"),
    }),
    "SpecificAdministratorModel": api.model('administrator', {
        "firstname": fields.String(required=True, example="Max", description="firstname"),
        "lastname": fields.String(required=True, example="Mustermann", description="lastname"),
    }),
}

responseSchema = {
}


@administrator_api.route('/')
@administrator_api.doc('all administrator actions')
class AdministratorService(Resource):

    @administrator_api.doc('create the first administrator')
    @administrator_api.expect(requestSchema["AdministratorModel"])
    def put(self):
        count: int = db.session.query(func.count(AdministratorModel.uuid)).first()[0]

        if count == 0:
            firstname = request.json["firstname"]
            lastname = request.json["lastname"]
            password = generate_password_hash(request.json["password"])

            admin = AdministratorModel.create(firstname, lastname, password)

            return { "result": True }
        else:
            return { "result": False }

    @administrator_api.doc('create an administrator')
    @administrator_api.expect(requestSchema["AdministratorModel"])
    @require_session
    def post(self, session):
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        password = generate_password_hash(request.json["password"])

        admin = AdministratorModel.create(firstname, lastname, password)

        return jsonify(admin.serialize)

    @administrator_api.doc('delete an administrator')
    @administrator_api.expect(requestSchema["SpecificAdministratorModel"])
    @require_session
    def delete(self, session):
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]

        admin = AdministratorModel.query.filter_by(firstname=firstname, lastname=lastname).first()

        db.session.delete(admin)
        db.session.commit()

        return { "result": True }


@administrator_api.route('/session/')
@administrator_api.doc('all administrator session actions')
class SessionAdministratorService(Resource):

    @administrator_api.doc('create an administrator session')
    @administrator_api.expect(requestSchema["AdministratorModel"])
    def put(self):
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        password = request.json["password"]

        admin = AdministratorModel.query.filter_by(firstname=firstname, lastname=lastname).first()

        if admin and check_password_hash(admin.password, password):
            session = SessionModel.create(admin)
            return jsonify(session.serialize)
        else:
            return { "result": False }

    @administrator_api.doc('get session')
    @require_session
    def get(self, session):
        return jsonify(session.serialize)

    @administrator_api.doc('delete session')
    @require_session
    def delete(self, session):
        db.session.delete(session)
        db.commit()

        return { "result": True }
