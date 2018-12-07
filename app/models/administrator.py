from api import db
from uuid import uuid4


class AdministratorModel(db.Model):
    __tablename__: str = "administrator"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    firstname: db.Column = db.Column(db.String(255), nullable=False)
    lastname: db.Column = db.Column(db.String(255), nullable=False)
    password: db.Column = db.Column(db.String(255), nullable=False)

    # add an role of the person (viewer, scanner, admin) or smth else

    @property
    def serialize(self):
        _ = self.uuid
        return self.__dict__

    @staticmethod
    def create(firstname: str, lastname: str, password: str) -> "AdministratorModel":
        uuid = str(uuid4()).replace('-', '')
        admin = AdministratorModel(uuid=uuid, password=password, firstname=firstname, lastname=lastname)

        # send email with token and information
        # maybe captcha

        db.session.add(admin)
        db.session.commit()

        return admin

    @staticmethod
    def check_admin() -> bool:
        # count the administrators here
        return False
