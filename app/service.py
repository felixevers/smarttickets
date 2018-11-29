from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

db: SQLAlchemy = SQLAlchemy()
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