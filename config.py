import os


class Config(object):
    ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = ENV == "development"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    BUCKET = os.environ.get("BUCKET", "spstest-dev")

    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "change-this-key-in-the-application-config"
    )
    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY", "change-this-key-in-the-application-config"
    )
    JWT_BLACKLIST_TOKEN_CHECKS = "access"
