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

        key = '_sa_instance_state'

        if key in dict:
            del dict[key]
        
        return self.__dict__

    @staticmethod
    def create(name: str) -> "RoomModel":
        uuid = str(uuid4()).replace('-', '')

        room: RoomModel = RoomModel(uuid=uuid, name=name)

        db.session.add(room)
        db.session.commit()

        return room
