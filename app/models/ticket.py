from api import db
from sqlalchemy import ForeignKey
#from sqlalchemy.orm import relationship


class TicketModel(db.Model):
    __tablename__: str = "ticket"

    code: db.Column = db.Column(db.String(13), primary_key=True, unique=True)
    customer: db.Column = db.Column(db.String(255), nullable=False)
    paid: db.Column = db.Column(db.Boolean, nullable=False)
    seat_id: db.Column(db.String(32), ForeignKey('seat.uuid'))
    meeting_id: db.Column(db.String(32), ForeignKey('meeting.uuid'))
    price_id: db.Column(db.String(32), ForeignKey('price.uuid'))

    #seat = relationship("SeatModel")
    #meeting = relationship("MeetingModel")
    #price = relationship("PriceModel")

    @property
    def serialize(self):
        _ = self.uuid
        return self.__dict__

    @staticmethod
    def create():
        pass
