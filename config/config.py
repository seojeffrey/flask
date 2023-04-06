# -*- coding: utf-8 -*-
import redis
from .cache import REDIS_URI
from .database import CONFIG_DATABASE_DB_URI


class Config:
    # https://flask.palletsprojects.com/en/2.2.x/config/
    SQLALCHEMY_DATABASE_URI = CONFIG_DATABASE_DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configure Redis for storing the session data on the server-side
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(REDIS_URI)
    FLASK_DEBUG = False
    TESTING = False
    SECRET_KEY = 'FLASK_SECRET_KEY'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    TESTING = True


class TestingConfig(Config):
    TESTING = True
