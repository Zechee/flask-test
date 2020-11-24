from db import db
from datetime import datetime
from sqlalchemy import ForeignKey, func

class OptionModel(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    option_name = db.Column(db.String, nullable=False, unique=True)
    option_length = db.Column(db.Integer)
    op_default = db.Column(db.String)
    invoke_name = db.Column(db.String, nullable=False, unique=True)
    status = db.Column(db.Integer, server_default='1')
    created_at = db.Column(db.DateTime, server_default=func.now())
    


    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
