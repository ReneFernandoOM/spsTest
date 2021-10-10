from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, ma
from marshmallow import fields


class ApiUserModel(db.Model):
    __tablename__ = "api_user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def set_hash_password(self):
        self.password_hash = generate_password_hash(self.password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_id(cls, _id: int) -> "ApiUserModel":
        return cls.query.get(_id)

    @classmethod
    def find_by_email(cls, email: str) -> "ApiUserModel":
        return cls.query.filter_by(email=email).first()


class ApiUserSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(attribute="password_hash")

    class Meta:
        model = ApiUserModel
        load_only = ("password",)
        dump_only = ("id",)
        exclude = ("password_hash", "admin")
        load_instance = True
