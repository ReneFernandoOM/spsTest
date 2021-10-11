from flask import Flask, jsonify
from app.extensions import api, db, ma, jwt, migrate


from config import Config
from app.resources.api_user import ApiUserRegister, ApiUser, ApiUserLogin, ApiUserLogout
from app.resources.client_user import ClientUser, ClientUserList
from app.resources.pet import Pet, PetList
from app.resources.pet_image import PetImage


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    ma.init_app(app)

    db.init_app(app)

    migrate.init_app(app, db)

    api.add_resource(ApiUserRegister, "/register")
    api.add_resource(ApiUserLogin, "/login")
    api.add_resource(ApiUserLogout, "/logout")
    api.add_resource(ApiUser, "/user/<int:user_id>")
    api.add_resource(ClientUser, "/client")
    api.add_resource(ClientUserList, "/clients")
    api.add_resource(Pet, "/pet")
    api.add_resource(PetList, "/pets")
    api.add_resource(PetImage, "/pet_image/<int:pet_id>")
    api.init_app(app)

    configure_jwt(app)

    return app


def configure_jwt(app):
    jwt.init_app(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        api_user = ApiUserModel.find_by_id(identity)
        if api_user.admin:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return bool(TokenBlockList.query.filter_by(jti=jwt_payload["jti"]).all())

    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        return jsonify({"mensaje": "Token ha sido revocado."})

    @jwt.expired_token_loader
    def expored_toke_response(jwt_header, jwt_payload):
        return jsonify({"mensaje": "Token ha expirado."})


from app import models
from app.models.api_user import ApiUserModel
from app.models.blocklist import TokenBlockList
