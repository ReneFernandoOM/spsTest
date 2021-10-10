from typing import List

from app.extensions import db, ma


class ClientUserModel(db.Model):
    __tablename__ = "client_user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)

    @classmethod
    def find_by_id(cls, _id: int) -> "ClientUserModel":
        return cls.query.get(_id)

    @classmethod
    def find_by_email(cls, email: str) -> "ClientUserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone_number: str) -> "ClientUserModel":
        return cls.query.filter_by(phone_number=phone_number).first()

    @classmethod
    def find_all(cls) -> List["ClientUserModel"]:
        return cls.query.all()

    @classmethod
    def find_by_email_and_phone(
        cls, email: str, phone_number: str
    ) -> "ClientUserModel":
        return cls.query.filter_by(email=email, phone_number=phone_number).first()


class ClientUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientUserModel
        dump_only = ("id",)
        load_instance = True
