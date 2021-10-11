from flask import request, Response
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.libs.image_helper import (
    upload_image_to_s3,
    get_image_from_s3,
    delete_image_from_s3,
)
from app.models.pet_image import ImageSchema
from app.models.pet import PetModel
from app.extensions import db


class PetImage(Resource):
    @classmethod
    @jwt_required()
    def post(cls, pet_id):
        pet = cls.get_pet_by_id(pet_id)

        if pet.image_s3_key:
            return {"mensaje": "La mascota ya cuenta con imagen"}, 400

        schema = ImageSchema()
        try:
            data = schema.load(request.files)
        except ValidationError as err:
            return err.messages, 400

        try:
            s3_key = upload_image_to_s3(data["image"], pet_id)
        except:
            return {"mensaje": "Error interno"}, 500

        if not s3_key:
            return {"mensaje": "Extensión inválida."}, 400

        pet.image_s3_key = s3_key
        db.session.commit()

        return {"mensaje": "Imagen guardada."}, 201

    @classmethod
    @jwt_required()
    def get(cls, pet_id):
        pet = cls.get_pet_by_id(pet_id)
        if not pet.image_s3_key:
            return {"mensaje": "No hay imagen para esa mascota."}, 404
        file = get_image_from_s3(pet.image_s3_key)
        return Response(
            file["Body"].read(),
            headers={
                "Content-Disposition": "attachment;filename=test.png",
                "Content-Type": "image/jpeg",
            },
        )

    @classmethod
    @jwt_required()
    def put(cls, pet_id):
        pet = cls.get_pet_by_id(pet_id)

        schema = ImageSchema()
        try:
            data = schema.load(request.files)
        except ValidationError as err:
            return err.messages, 400

        try:
            s3_key = upload_image_to_s3(data["image"], pet_id)
        except:
            return {"mensaje": "Error interno"}, 500

        if not s3_key:
            return {"mensaje": "Extensión inválida."}, 400

        if pet.image_s3_key:
            delete_image_from_s3(pet.image_s3_key)

        pet.image_s3_key = s3_key
        db.session.commit()
        return {"mensaje": "Imagen guardada."}, 201

    @classmethod
    @jwt_required()
    def delete(cls, pet_id):
        pet = cls.get_pet_by_id(pet_id)

        if pet.image_s3_key:
            delete_image_from_s3(pet.image_s3_key)
            pet.image_s3_key = None
            db.session.commit()

        return {"mensaje": "Imagen borrada"}, 200

    @classmethod
    def get_pet_by_id(cls, pet_id):
        pet = PetModel.find_by_id(pet_id)
        if not pet:
            abort(404, mensaje="Usuario no encontrado")

        return pet
