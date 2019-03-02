from api import db
from uuid import uuid4
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta
from models.room import RoomModel

class SeatModel(db.Model):
    __tablename__: str = "seat"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    room_id: db.Column = db.Column(db.String(32), ForeignKey('room.uuid'))
    block: db.Column = db.Column(db.Integer(), nullable=False)
    row: db.Column = db.Column(db.Integer(), nullable=False)
    type: db.Column = db.Column(db.Integer(), nullable=False)

    @property
    def serialize(self):
        dict = {
            "uuid": self.uuid,
            "room_id": self.room_id,
            "block": self.block,
            "row": self.row,
            "type": self.type,
        }

        return dict

    @staticmethod
    def create(room: RoomModel, block: int, row: int, type: int=0) -> "SeatModel":
        uuid = str(uuid4()).replace('-', '')

        seat: SeatModel = SeatModel(uuid=uuid, room_id=room, block=block, row=row, type=type)

        db.session.add(seat)
        db.session.commit()

        return seat
