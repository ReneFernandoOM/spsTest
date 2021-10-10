from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt,
)

from app.models.api_user import ApiUserModel, ApiUserSchema
from app.models.blocklist import TokenBlockListSchema
from app.resources import admin_required
from app.extensions import db


class ApiUserRegister(Resource):
    def post(self):
        user_schema = ApiUserSchema()
        new_api_user = user_schema.load(request.get_json())

        if ApiUserModel.find_by_email(new_api_user.email):
            return {"mensaje": "Ese email ya se encuentra en uso."}, 400

        new_api_user.set_hash_password()
        db.session.add(new_api_user)
        db.session.commit()

        return {
            "mensaje": "Usuario creado.",
            "usuario": user_schema.dump(new_api_user),
        }, 201


class ApiUserLogin(Resource):
    @classmethod
    def post(cls):
        user_schema = ApiUserSchema()
        user_data = user_schema.load(request.get_json())

        user = ApiUserModel.find_by_email(user_data.email)
        if user and user.check_password(user_data.password_hash):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200

        return {"mensaje": "Las credenciales son inválidas."}, 401


class ApiUserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        schema = TokenBlockListSchema()
        jwt = get_jwt()
        logout_dict = {"jti": jwt["jti"], "api_user_id": jwt["sub"]}
        token_block = schema.load(logout_dict)
        db.session.add(token_block)
        db.session.commit()

        return {"mensaje": "Usuario logged out"}


class ApiUser(Resource):
    @classmethod
    @admin_required()
    def get(cls, user_id: int):
        schema = ApiUserSchema()
        api_user = ApiUserModel.find_by_id(user_id)
        if api_user:
            return schema.dump(api_user), 200
        return {"mensaje": "Usuario no encontrado"}, 404

    @classmethod
    @admin_required()
    def delete(cls, user_id: int):
        api_user = ApiUserModel.find_by_id(user_id)
        if api_user:
            db.session.delete(api_user)
            db.session.commit()

        return {"mensaje": "Usuario borrado"}, 200
