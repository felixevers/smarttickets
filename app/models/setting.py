from api import db


class SettingModel(db.Model):
    __tablename__: str = "setting"

    key: db.Column = db.Column(db.String(255), primary_key=True, unique=True)
    value: db.Column = db.Column(db.String(510), nullable=False)

    @property
    def serialize(self):
        dict = self.__dict__

        key = '_sa_instance_state'

        if key in dict:
            del dict[key]

        return dict

    @staticmethod
    def create(key: str, value: str) -> 'SettingModel':
        setting = SettingModel(key=key, value=value)

        db.session.add(setting)
        db.session.commit()

        return setting
