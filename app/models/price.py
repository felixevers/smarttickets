from api import db
from sqlalchemy.orm import relationship
from uuid import uuid4
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta

from models.meeting import MeetingModel


class PriceModel(db.Model):
    __tablename__: str = "price"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    name: db.Column = db.Column(db.String(255), nullable=False)
    description: db.Column = db.Column(db.String(255), nullable=False)
    value: db.Column = db.Column(db.Integer(), nullable=False)
    meeting_id: db.Column(db.String(32), ForeignKey('meeting.uuid'))

    meeting = relationship(MeetingModel, backref="meeting")

    @property
    def serialize(self):
        _ = self.uuid
        return self.__dict__

    @staticmethod
    def create():
        pass