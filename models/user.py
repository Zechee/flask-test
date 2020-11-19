from db import db
from flask_bcrypt import Bcrypt


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80))

    # @property
    # def password(self):
    #     raise ValueError('write only!')

    # @password.setter
    # def password(self, value):
    #     self.password_hash = bcrypt.generate_password_hash(value)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def set_password(self, password):
        self.password = Bcrypt().generate_password_hash(password)

    def check_password(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
