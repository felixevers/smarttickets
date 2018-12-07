from flask_restplus import Namespace, Resource, fields, abort
from api import api
from flask import request
from models.customer import CustomerModel

customer_api = Namespace('customer')

requestSchema = {
    "CustomerCreateSchema": api.model("create request", {
        "email": fields.String(required=True, example="max@mustmann.de", description="email address"),
        "firstname": fields.String(required=True, example="Max", description="firstname"),
        "lastname": fields.String(required=True, example="Mustermann", description="lastname"),
        "address": fields.String(required=True, example="Musterstreet 123",
                                 description="street with addition of the housenumber"),
        "place": fields.String(required=True, example="Mustercity", description="place")
    }),
    "CustomerInformationSchema": api.model("get information request", {
        "token": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                               description="auth-token (like an password)")
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

        return customer.serialize


@customer_api.route('/<string:uuid>')
@customer_api.doc('all possible customer actions')
class CustomerService(Resource):

    @customer_api.doc('returns general information about the customer')
    @customer_api.expect(requestSchema["CustomerInformationSchema"])
    @customer_api.marshal_with(responseSchema["CustomerGeneralInformationSchema"])
    @customer_api.response(404, "Not Found", {})
    def get(self, uuid: str):
        token: str = request.json["token"]
        customer: CustomerModel = CustomerModel.query.filter_by(uuid=uuid, token=token).first()

        if not customer:
            abort(404, "invalid customer")

        return customer.serialize
