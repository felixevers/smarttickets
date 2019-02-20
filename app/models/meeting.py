from api import db
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import ForeignKey
from datetime import datetime

class MeetingModel(db.Model):
    __tablename__: str = "meeting"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    name: db.Column = db.Column(db.String(255), nullable=False)
    description: db.Column = db.Column(db.String(255), nullable=False)
    date: db.Column = db.Column(db.Integer())
    start: db.Column = db.Column(db.Integer())
    stop: db.Column = db.Column(db.Integer())
    room: db.Column = db.Column(db.String(32), ForeignKey('room.uuid'))

    @property
    def serialize(self):
        _ = self.uuid

        key = '_sa_instance_state'

        if key in dict:
            del dict[key]
        
        return self.__dict__

    @staticmethod
    def create(name: str, description: str, room, date, start, stop) -> "MeetingModel":
        uuid = str(uuid4()).replace('-', '')

        meeting: MeetingModel = MeetingModel(uuid=uuid, name=name, description=description, room=room, date=date, start=start, stop=stop)

        db.session.add(meeting)
        db.session.commit()

        return meeting
