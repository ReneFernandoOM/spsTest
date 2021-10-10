from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.models.pet import PetModel, PetSchema
from app.models.client_user import ClientUserModel
from app.extensions import db


class Pet(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        params = request.args.to_dict()
        pet = cls.get_pet_by_id(params)
        if pet:
            schema = PetSchema()
            return {"mascota": schema.dump(pet)}, 200

        return {"mensaje": "Mascota no encontrada"}, 404

    @classmethod
    @jwt_required()
    def post(cls):
        schema = PetSchema()
        try:
            pet = schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if not ClientUserModel.find_by_id(pet.owner_id):
            return {"mensaje": "No hay un dueño con ese id."}, 400

        db.session.add(pet)
        db.session.commit()
        return {"mensaje": schema.dump(pet)}, 201

    @classmethod
    @jwt_required()
    def put(cls):
        params = request.args.to_dict()
        pet = cls.get_pet_by_id(params)
        schema = PetSchema()
        new_pet_info = schema.load(request.get_json())
        if pet:
            pet.name = new_pet_info.name
            pet.weight = new_pet_info.weight
            pet.height = new_pet_info.height
            pet.tipo_animal = new_pet_info.tipo_animal
            pet.owner_id = new_pet_info.owner_id
            return_code = 200
        else:
            pet = new_pet_info
            db.session.add(pet)
            return_code = 201
        db.session.commit()

        return schema.dump(pet), return_code

    @classmethod
    @jwt_required()
    def delete(cls):
        params = request.args.to_dict()
        pet = cls.get_pet_by_id(params)

        if pet:
            db.session.delete(pet)
            db.session.commit()
            return {"mensaje": "La mascota ha sido borrada"}, 200

        return {"mensaje": "No se ha encontrado la mascota"}, 404

    @classmethod
    def get_pet_by_id(cls, params):
        if "id" not in params:
            return abort(
                400,
                mensaje="'id' debe de estar presente en los parametros del endpoint",
            )

        return PetModel.find_by_id(params["id"])


class PetList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        params = request.args.to_dict()
        if "owner_id" in params:
            schema = PetSchema(many=True, exclude=["owner"])
            owner = ClientUserModel.find_by_id(params["owner_id"])
            if owner:
                return {"mascotas": schema.dump(owner.pets)}, 200
            return {"mensaje": "No existe un dueño con ese id"}, 404
        schema = PetSchema(many=True)
        pets = PetModel.find_all()
        return {"mascotas": schema.dump(pets)}, 200
