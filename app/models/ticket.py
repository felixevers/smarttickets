from api import db
from uuid import uuid4
from sqlalchemy import ForeignKey


class TicketModel(db.Model):
    __tablename__: str = "ticket"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    customer: db.Column = db.Column(db.String(32), ForeignKey('customer.uuid'))
    paid: db.Column = db.Column(db.Boolean(), nullable=False)
    seat_id: db.Column = db.Column(db.String(32), ForeignKey('seat.uuid'))
    meeting_id: db.Column = db.Column(db.String(32), ForeignKey('meeting.uuid'))
    price_id: db.Column = db.Column(db.String(32), ForeignKey('price.uuid'))

    @property
    def serialize(self):
        dict = self.__dict__

        key = '_sa_instance_state'

        if key in dict:
            del dict[key]

        return dict

    @staticmethod
    def create(customer, meeting, seat, price):
        uuid = str(uuid4()).replace('-', '')

        ticket: TicketModel = TicketModel(uuid=uuid, customer=customer.uuid, paid=False, seat_id=seat.uuid, meeting_id=meeting.uuid, price_id=price.uuid)

        db.session.add(ticket)
        db.session.commit()

        return ticket
