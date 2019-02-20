from api import db
from uuid import uuid4
from sqlalchemy import ForeignKey

class SessionModel(db.Model):
    __tablename__: str = "session"

    uuid: db.Column = db.Column(db.String(32), primary_key=True, unique=True)
    administrator: db.Column = db.Column(db.String(255), ForeignKey('administrator.uuid'))
    broken: db.Column = db.Column(db.Boolean(), nullable=False)

    @property
    def serialize(self):
        dict = {
            "uuid": self.uuid,
            "administrator": self.administrator,
            "broken": self.broken,
        }

        print(dict)

        return dict

    @staticmethod
    def create(administrator) -> "SessionModel":
        uuid = str(uuid4()).replace('-', '')
        session = SessionModel(uuid=uuid, administrator=administrator.uuid, broken=False)

        db.session.add(session)
        db.session.commit()

        return session
