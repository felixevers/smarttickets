from api import db
from sqlalchemy.orm import relationship
from uuid import uuid4


class PriceModel(db.Model):
    __tablename__: str = "price"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    name: db.Column = db.Column(db.String(255), nullable=False)
    description: db.Column = db.Column(db.String(255), nullable=False)
    value: db.Column = db.Column(db.Float(), nullable=False)

    @property
    def serialize(self):
        dict = self.__dict__

        key = '_sa_instance_state'

        if key in dict:
            del dict[key]

        return dict

    @staticmethod
    def create(name, description, value):
        uuid = str(uuid4()).replace('-', '')

        price: PriceModel = PriceModel(uuid=uuid, name=name, description=description, value=value)

        db.session.add(price)
        db.session.commit()

        return price
