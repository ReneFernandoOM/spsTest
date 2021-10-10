from marshmallow.decorators import post_load
from app.extensions import db, ma
from marshmallow import fields

from app.models.client_user import ClientUserSchema


class PetModel(db.Model):
    __tablename__ = "pet"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    weight = db.Column(db.Float(precision=2), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    tipo_animal = db.Column(db.String(50), nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("client_user.id"), nullable=False)
    owner = db.relationship("ClientUserModel", backref="pets", lazy="joined")

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()


class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PetModel
        load_only = ("owner_id",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True

    owner = fields.Nested(ClientUserSchema(only=["id", "email"]))

    @post_load
    def standarize_strings(self, data, **kwargs):
        data.name = data.name.title()
        data.tipo_animal = data.tipo_animal.lower()
        return data
