from datetime import datetime

from app.extensions import db, ma


class TokenBlockList(db.Model):
    __tablename__ = "token_block_list"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    api_user_id = db.Column(db.Integer, db.ForeignKey("api_user.id"), nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship("ApiUserModel", lazy="joined")


class TokenBlockListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TokenBlockList
        dump_only = ("revoked_at",)
        exclude = ("id",)
        load_instance = True
        include_fk = True
