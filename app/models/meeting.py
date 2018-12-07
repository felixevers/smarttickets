from api import db
from uuid import uuid4
from datetime import datetime, timedelta


class MeetingModel(db.Model):
    __tablename__: str = "meeting"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    name: db.Column = db.Column(db.String(255), nullable=False)
    description: db.Column = db.Column(db.String(255), nullable=False)
    date: db.Column = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start: db.Column = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stop: db.Column = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def serialize(self):
        _ = self.uuid
        return self.__dict__

    @staticmethod
    def create(name: str, description: str) -> "MeetingModel":
        uuid = str(uuid4()).replace('-', '')

        meeting: MeetingModel = MeetingModel(uuid=uuid, name=name, description=description)

        db.session.add(meeting)
        db.session.commit()

        return meeting
