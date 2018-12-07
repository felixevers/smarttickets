from api import db
from uuid import uuid4
from datetime import datetime, timedelta


class RoomModel(db.Model):
    __tablename__: str = "room"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    name: db.Column = db.Column(db.String(255), nullable=False)


    @property
    def serialize(self):
        _ = self.uuid
        return self.__dict__

    @staticmethod
    def create():
        pass
