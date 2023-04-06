import datetime
from flask import request, session

from api import login_required
from app import app
from const.response_code import ResponseCode
from library.api_message import ApiMessage
from model import db
from model.model import BoardArticle
"""
3. BoardArticle APIs : 게시판 글 CRUD
"""


# 1. Create API : *title*, *content* 를 입력받아 특정 게시판에 새로운 글을 작성합니다.
@app.route('/api/boards/<int:board_id>/board-articles', methods=['PUT'])
@login_required
def create_board_articles(board_id):  # put application's code here
    params = request.get_json()
    article_title = params["title"]
    article_contents = params["contents"]
    email = session['email']
    if not all((article_contents, article_title)):
        return ApiMessage(ResponseCode.ARTICLE_NO_CONTENTS_OR_TITLE)
    new_board_article = BoardArticle(owner=email, title=article_title, board_id=board_id, content=article_contents,
                                     create_datetime=datetime.datetime.utcnow(),
                                     last_update_datetime=datetime.datetime.utcnow())
    db.add(new_board_article)
    db.commit()
    return ApiMessage()


# 2. Get API : 특정 게시판 글의 내용을 가져옵니다.
@app.route('/api/boards/<int:board_id>/board-articles/<int:article_id>')
def get_board_articles(board_id, article_id):
    # pagenation
    """
    #
    email = session['email']
    table_result = db.query(BoardArticle).filter(BoardArticle.owner == email, BoardArticle.board_id == board_id,
                                                 BoardArticle.id == article_id).first() or list()
    """

    table_result = db.query(BoardArticle).filter(BoardArticle.board_id == board_id,
                                                 BoardArticle.id == article_id).first() or dict()
    return ApiMessage(result=table_result)


# 3. Update API : 특정 게시판 글의 *title*, *content*를 변경합니다.
@app.route('/api/boards/<int:board_id>/board-articles/<int:article_id>', methods=['POST'])
@login_required
def update_board_articles(board_id, article_id):
    params = request.get_json()
    article_title = params.get("title")
    article_contents = params.get("contents")
    email = session['email']
    if not any((article_title, article_contents)):
        return ApiMessage(ResponseCode.ARTICLE_NO_CONTENTS_OR_TITLE)

    table_result = db.query(BoardArticle).filter(BoardArticle.board_id == board_id,
                                                 BoardArticle.id == article_id).first()

    if not table_result:
        return ApiMessage(ResponseCode.BOARD_NOT_EXIST)
    elif table_result.owner != email:
        return ApiMessage(ResponseCode.ARTICLE_PERMISSION_DENIED)
    else:
        if article_title:
            table_result.title = article_title
        if article_contents:
            table_result.content = article_contents
        db.add(table_result)
        db.commit()
    return ApiMessage()


# 4. Delete API : 특정 게시판 글을 제거합니다.
@app.route('/api/boards/<int:board_id>/board-articles/<int:article_id>', methods=['DELETE'])
@login_required
def delete_board_articles(board_id, article_id):
    email = session['email']

    table_result = db.query(BoardArticle).filter(BoardArticle.board_id == board_id,
                                                 BoardArticle.id == article_id).first()
    if not table_result:
        return ApiMessage(ResponseCode.BOARD_ARTICLE_NOT_EXISTS)
    elif table_result.owner != email:
        return ApiMessage(ResponseCode.ARTICLE_PERMISSION_DENIED)
    db.delete(table_result)
    db.commit()
    return ApiMessage()

