from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from flask_mail import Mail
from flask_qrcode import QRcode

db: SQLAlchemy = SQLAlchemy()
mail: Mail = Mail()
api: Api = Api(
    version='1.0',
    title="smarttickets",
    description="application programming interface of smarttickets",
    authorizations={
        "token": {
            "type": "apiKey",
            "in": "header",
            "name": "Token"
        }
    },
    doc='/swagger/'
)
qrcode: QRcode = QRcode()
