from api import db
from uuid import uuid4


class CustomerModel(db.Model):
    __tablename__: str = "customer"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    token: db.Column = db.Column(db.String(32), unique=True, nullable=False)
    firstname: db.Column = db.Column(db.String(255), nullable=False)
    lastname: db.Column = db.Column(db.String(255), nullable=False)
    email: db.Column = db.Column(db.String(255), nullable=False)
    address: db.Column = db.Column(db.String(255), nullable=False)
    place: db.Column = db.Column(db.String(255), nullable=False)

    @property
    def serialize(self):
        _ = self.uuid

        dict = self.__dict__

        key = '_sa_instance_state'

        if key in dict:
            del dict[key]

        return dict

    @staticmethod
    def create(firstname: str, lastname: str, email: str, address: str, place: str) -> "CustomerModel":
        uuid = str(uuid4()).replace('-', '')
        token = str(uuid4()).replace('-', '')
        customer = CustomerModel(uuid=uuid, token=token, firstname=firstname, lastname=lastname,
                                 email=email, address=address, place=place)

        # send email with token and information
        # maybe captcha

        db.session.add(customer)
        db.session.commit()

        return customer
