import os


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = "change-this-key-in-the-application-config"

    JWT_SECRET_KEY = "change-this-key-to-something-different-in-the-application-config"
    JWT_BLACKLIST_TOKEN_CHECKS = "access"
