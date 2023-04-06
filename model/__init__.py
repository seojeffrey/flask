from sqlalchemy.orm import sessionmaker, scoped_session
from library.custom_json_encoder import AlchemyEncoder

db = None


def init_database(app):
    # thread 가 여러개 일때 connection 을 관리 해줌
    Session = scoped_session(sessionmaker(bind=app.database))
    # session 이라 하면 헷깔리니 db 로 변경
    global db
    db = Session()
    # 인코더 추가
    app.json_encoder = AlchemyEncoder
