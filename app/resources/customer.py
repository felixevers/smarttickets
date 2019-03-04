from flask_restplus import Namespace, Resource, fields, abort
from api import api, db, mail
from flask import request
from models.customer import CustomerModel
from models.setting import SettingModel
from config import config
from session import require_session
from flask_mail import Mail, Message

customer_api = Namespace('customer')

requestSchema = {
    "CustomerCreateSchema": api.model("create request", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                            description="uuid"),
        "email": fields.String(required=True, example="max@mustmann.de", description="email address"),
        "firstname": fields.String(required=True, example="Max", description="firstname"),
        "lastname": fields.String(required=True, example="Mustermann", description="lastname"),
        "address": fields.String(required=True, example="Musterstreet 123",
                                 description="street with addition of the housenumber"),
        "place": fields.String(required=True, example="Mustercity", description="place")
    }),
    "CustomerInformationSchema": api.model("get information request", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                               description="uuid")
    })
}

responseSchema = {
    "CustomerGeneralInformationSchema": api.model("information response", {
        "uuid": fields.String(example="12abc34d5efg67hi89j1klm2nop3pqrs", description="uuid of customer"),
        "email": fields.String(example="max@mustmann.de", description="email address"),
        "firstname": fields.String(example="Max", description="firstname"),
        "lastname": fields.String(example="Mustermann", description="lastname"),
        "address": fields.String(example="Musterstreet 123", description="street with addition of the housenumber"),
        "place": fields.String(exmaple="Mustercity", description="place")
    })
}


@customer_api.route('/')
@customer_api.doc('create customer')
class CustomerCreateService(Resource):

    @customer_api.doc('get all customers')
    @require_session
    def get(self, session):
        return {
            "customers": [customer.serialize for customer in CustomerModel.query.all()]
        }

    @customer_api.doc('creates a customer')
    @customer_api.expect(requestSchema["CustomerCreateSchema"])
    @customer_api.marshal_with(responseSchema["CustomerGeneralInformationSchema"])
    def put(self):
        email = request.json["email"]
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        address = request.json["address"]
        place = request.json["place"]

        customer: CustomerModel = CustomerModel.create(firstname, lastname, email, address, place)

        if config["MAIL_ENABLED"]:
            msg_title = SettingModel.query.filter_by(key="customer_mail_title").first().value
            msg_content = SettingModel.query.filter_by(key="customer_mail_content").first().value

            bcc = SettingModel.query.filter_by(key="mail_bcc").first()

            msg = Message(msg_title, recipients=[customer.email])

            if bcc and bcc.value != '':
                msg.bcc = bcc.value

            customer_url = str(request.host_url) + 'f/customer/' + customer.uuid

            msg_content = msg_content.replace('<name>', firstname + ' ' + lastname)
            msg_content = msg_content.replace('<customer>', '<a href="' + customer_url + '">' + customer_url + '</a>')
            msg_content = msg_content.replace('\n', '<br>')

            msg.html = msg_content

            mail.send(msg)

        return customer.serialize


@customer_api.route('/<string:uuid>')
@customer_api.doc('all possible customer actions')
class CustomerService(Resource):

    @customer_api.doc('returns general information about the customer')
    @customer_api.expect(requestSchema["CustomerInformationSchema"])
    @customer_api.marshal_with(responseSchema["CustomerGeneralInformationSchema"])
    @customer_api.response(404, "Not Found", {})
    def get(self, uuid: str):
        customer: CustomerModel = CustomerModel.query.filter_by(uuid=uuid).first()

        if not customer:
            abort(404, "invalid customer")

        return customer.serialize

    @customer_api.doc('deletes the customer')
    @customer_api.response(404, "Not Found", {})
    @require_session
    def delete(self, uuid: str, session):
        customer: CustomerModel = CustomerModel.query.filter_by(uuid=uuid).first()

        if not customer:
            abort(404, "invalid customer")

        db.session.delete(customer)
        db.session.commit()

        return customer.serialize
