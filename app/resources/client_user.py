from typing import Dict, Union

from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError, EXCLUDE

from app.extensions import db
from app.models.client_user import ClientUserModel, ClientUserSchema


class ClientUser(Resource):
    @classmethod
    @jwt_required()
    def get(self):
        params = request.args.to_dict()
        client_user = self.get_client_user_by_email_or_phone(params)
        if client_user:
            schema = ClientUserSchema()
            return {"usuario": schema.dump(client_user)}

        return {"mensaje": "Usuario no encontrado"}, 404

    @classmethod
    @jwt_required()
    def post(self):
        schema = ClientUserSchema()
        try:
            new_client_user = schema.load(request.get_json(), unknown=EXCLUDE)
        except ValidationError as errors:
            return errors.messages, 400

        if ClientUserModel.find_by_phone(new_client_user.phone_number):
            return {"mensaje": "Telefono ya existe."}, 400
        elif ClientUserModel.find_by_email(new_client_user.email):
            return {"mensaje": "Email ya existe."}, 400

        try:
            db.session.add(new_client_user)
            db.session.commit()
        except:
            return {"mensaje": "Error interno"}, 500

        return schema.dump(new_client_user), 201

    @classmethod
    @jwt_required()
    def put(self):
        params = request.args.to_dict()
        payload = request.get_json()
        schema = ClientUserSchema()
        client_new_info = schema.load(payload)

        client_user = self.get_client_user_by_email_or_phone(params)

        # Comprobar que el email/phone number sean distintos al cliente (en caso de haberlo)
        phone_client_user = ClientUserModel.find_by_phone(client_new_info.phone_number)
        email_client_user = ClientUserModel.find_by_email(client_new_info.email)
        if phone_client_user and client_user != phone_client_user:
            return {"mensaje": "Telefono ya existe."}, 400
        elif email_client_user and client_user != email_client_user:
            return {"mensaje": "Email ya existe."}, 400

        if client_user:
            client_user.name = client_new_info.name
            client_user.last_name = client_new_info.last_name
            client_user.email = client_new_info.email
            client_user.phone_number = client_new_info.phone_number
        else:
            db.session.add(client_new_info)

        db.session.commit()

        return schema.dump(client_new_info), 200

    @classmethod
    @jwt_required()
    def delete(self):
        params = request.args.to_dict()
        client_user = self.get_client_user_by_email_or_phone(params)

        if client_user:
            db.session.delete(client_user)
            db.session.commit()
            return {"message": "El usuario ha sido borrado."}, 200

        return {"message": "El usuario no existe."}, 404

    @classmethod
    def get_client_user_by_email_or_phone(
        cls, params: Dict
    ) -> Union[Dict, "ClientUser", None]:
        """
        Verifica que los parametros del query esten correctos y devuelve el "ClientUser"
        en caso de que exista.
        """
        if {"email", "phone_number"} <= params.keys():
            client_user = ClientUserModel.find_by_email_and_phone(
                params["email"], params["phone_number"]
            )
        elif "email" in params.keys():
            client_user = ClientUserModel.find_by_email(params["email"])
        elif "phone_number" in params:
            client_user = ClientUserModel.find_by_phone(params["phone_number"])
        else:
            return abort(
                400,
                mensaje="'email' o 'phone_number' deben de estar presentes en los parametros del endpoint.",
            )

        return client_user


class ClientUserList(Resource):
    @classmethod
    def get(cls):
        schema = ClientUserSchema(many=True)
        print(ClientUserModel.find_all())
        return {"clientes": schema.dump(ClientUserModel.find_all())}, 200
