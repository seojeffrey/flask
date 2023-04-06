from flask import Flask
from sqlalchemy import create_engine

from config.database import DB_POOL_SIZE, DB_MAX_OVERFLOW, DB_POOL_RECYCLE
from model import init_database


def create_app():
    flask_app = Flask(__name__)

    flask_app.config.from_object('config.config.DevelopmentConfig')

    flask_app.debug = flask_app.config['FLASK_DEBUG']
    flask_app.app_context().push()
    # sql alchemy
    database = create_engine(flask_app.config['SQLALCHEMY_DATABASE_URI'], echo=flask_app.config['DEBUG'],
                             pool_size=DB_POOL_SIZE, pool_recycle=DB_POOL_RECYCLE,
                             max_overflow=DB_MAX_OVERFLOW)
    flask_app.database = database
    init_database(flask_app)
    return flask_app


app = create_app()


from api.user import *
from api.board import *
from api.board_article import *
if __name__ == '__main__':
    app.run()
