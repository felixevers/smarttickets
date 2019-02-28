from flask import Flask
from flask_mail import Mail

from resources.render import register_render
from resources.customer import customer_api
from resources.setting import setting_api
from resources.meeting import meeting_api
from resources.price import price_api
from resources.room import room_api
from resources.seat import seat_api
from resources.ticket import ticket_api
from resources.administrator import administrator_api
from resources.download import register_download

from config import config
from api import db, api, mail
from flask_cors import CORS
from time import sleep

# only imported to create the tables (remove after finishing the resources)
from models.customer import CustomerModel
from models.meeting import MeetingModel
from models.price import PriceModel
from models.room import RoomModel
from models.seat import SeatModel
from models.setting import SettingModel
from models.customer import CustomerModel
from models.ticket import TicketModel
from models.administrator import AdministratorModel

import os


def create_app() -> Flask:
    frontend = os.path.abspath(config["FRONTEND"])
    app: Flask = Flask("smarttickets")

    app.config.update(**config)

    with app.app_context():
        if config["CROSS_ORIGIN"]:
            CORS(app)

        if config["MAIL"]:
            mail.init_app(app)

        register_render(app)
        register_download(app)

        register_extensions(app)

        register_namespaces()

        setup_database()


    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    api.init_app(app)


def register_namespaces() -> None:
    api.add_namespace(customer_api)
    api.add_namespace(setting_api)
    api.add_namespace(meeting_api)
    api.add_namespace(price_api)
    api.add_namespace(room_api)
    api.add_namespace(seat_api)
    api.add_namespace(ticket_api)
    api.add_namespace(administrator_api)


def setup_database() -> None:
    while True:
        try:
            db.create_all()
            break
        except Exception as e:
            raise e
            sleep(2)


if __name__ == '__main__':
    app: Flask = create_app()
    app.run(host='0.0.0.0', port=5000)
