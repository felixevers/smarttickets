from flask_restplus import Namespace, Resource, fields, abort
from api import api, db
from flask import request
from models.price import PriceModel
from session import require_session

price_api = Namespace('price')

requestSchema = {
    "CreatePriceModel": api.model("create price", {
        "name": fields.String(required=True, example="Adults",
                              description="name of price"),
        "description": fields.String(required=True, example="person above 18 years",
                                     description="filter for of price"),
        "value": fields.Integer(required=True, example="15",
                                     description="amount of price")
    }),
    "SpecificPriceModel": api.model("specific price", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of price"),
    })
}

responseSchema = {
    "PriceModel": api.model("price", {
        "uuid": fields.String(required=True, example="12abc34d5efg67hi89j1klm2nop3pqrs",
                              description="uuid of price"),
        "name": fields.String(required=True, example="Adults",
                              description="name of price"),
        "description": fields.String(required=True, example="person above 18 years",
                                     description="filter for of price"),
        "value": fields.Integer(required=True, example="15",
                                     description="amount of price")
    }),
    "SuccessModel": api.model("success", {
        "result": fields.Boolean(required=True)
    })
}

@price_api.route('/')
@price_api.doc('general price actions')
class GeneralPriceService(Resource):

    @price_api.doc('create a price')
    @price_api.expect(requestSchema["CreatePriceModel"])
    @price_api.marshal_with(responseSchema["PriceModel"])
    @require_session
    def put(self, session):
        name = request.json["name"]
        description = request.json["description"]
        value = request.json["value"]

        price: PriceModel = PriceModel.create(name, description, value)

        return price.serialize

    @price_api.doc('get all prices')
    def get(self):
        prices: list = PriceModel.query.all()

        return {
            'prices': [p.serialize for p in prices]
            }


@price_api.route('/<string:uuid>')
@price_api.doc('specific price actions')
class SpecificPriceService(Resource):

    @price_api.doc('get a price')
    @price_api.expect(requestSchema["SpecificPriceModel"])
    @price_api.marshal_with(responseSchema["PriceModel"])
    @price_api.response(404, "Not Found", {})
    def get(self, uuid):
        price: PriceModel = PriceModel.query.filter_by(uuid=uuid).first()

        return price.serialize

    @price_api.doc('delete a price')
    @price_api.expect(requestSchema["SpecificPriceModel"])
    @price_api.marshal_with(responseSchema["SuccessModel"])
    @price_api.response(404, "Not Found", {})
    @require_session
    def delete(self, uuid, session):
        price: PriceModel = PriceModel.query.filter_by(uuid=uuid).first()

        db.session.delete(price)
        db.session.commit()

        return True

    @price_api.doc('update a price')
    @price_api.expect(requestSchema["SpecificPriceModel"])
    @price_api.marshal_with(responseSchema["PriceModel"])
    @price_api.response(404, "Not Found", {})
    @require_session
    def post(self, uuid, session):
        name = request.json["name"]
        description = request.json["description"]
        value = request.json["value"]

        price: PriceModel = PriceModel.query.filter_by(uuid=uuid).first()

        price.name = name
        price.description = description
        price.value = value

        db.session.commit()

        return price.serialize
