# -*- coding: utf-8 -*-
import datetime
from flask import request, session
from sqlalchemy import text

from api import login_required
from app import app
from const.response_code import ResponseCode
from library.api_message import ApiMessage
from model import db
from model.model import Board, BoardArticle

"""
게시판 CRUD
"""


# 1. Create API : *name* 을 입력받아 새로운 게시판을 만듭니다.
@app.route('/api/boards', methods=['PUT'])
@login_required
def create_board():  # put application's code here
    params = request.get_json()
    board_name = str(params["name"]).strip()
    email = str(session['email']).strip()
    if not board_name:
        return ApiMessage(result_code=ResponseCode.BOARD_NAME_NOT_EXIST)
    new_board = Board(owner=email, name=board_name, create_datetime=datetime.datetime.utcnow())
    db.add(new_board)
    db.commit()
    return ApiMessage()


# 2. List API : 게시판 목록을 가져옵니다.
@app.route('/api/boards')
def get_boards():
    # pagenation
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        page = 1
        limit = 10

    # 유저가 보는 관점에서 0번부터가 아니기에 1빼줌
    page -= 1
    """
    # 모든 유저의 게시판을 의미하는 것일듯?
     email = session['email']

    table_result = db.query(Board).filter(Board.owner == email).\
        order_by(Board.create_datetime).offset(page*limit).limit(limit).all()
    
    # max page 계산
    table_count = db.query(Board).filter(Board.owner == email).count()
    """
    table_result = db.query(Board).order_by(Board.create_datetime).offset(page*limit).limit(limit).all()

    # max page 계산
    table_count = db.query(Board).count()
    max_pages = int(table_count / limit) + (1 if table_count % limit > 0 else 0)

    return ApiMessage(max_pages=max_pages, result=table_result)


# 3. Update API : 특정 게시판의 *name* 을 변경합니다.
@app.route('/api/boards/<int:board_id>/', methods=['POST'])
@login_required
def update_board(board_id):
    params = request.get_json()
    board_name = params["name"]

    email = session['email']
    table_result = db.query(Board).filter(Board.id == board_id).first()

    if not table_result:
        return ApiMessage(ResponseCode.BOARD_NOT_EXIST)
    elif table_result.owner != email:
        return ApiMessage(ResponseCode.BOARD_PERMISSION_DENIED)
    else:
        table_result.name = board_name
        db.add(table_result)
        db.commit()
    return ApiMessage()


# 4. Delete API : 특정 게시판을 제거합니다.
@app.route('/api/boards/<int:board_id>/', methods=['DELETE'])
@login_required
def delete_boards(board_id):
    email = session['email']

    table_result = db.query(Board).filter(Board.id == board_id).first()
    if not table_result:
        return ApiMessage(ResponseCode.BOARD_NOT_EXIST)
    elif table_result.owner != email:
        return ApiMessage(ResponseCode.BOARD_PERMISSION_DENIED)

    # article 정리
    target_article = db.query(BoardArticle).filter(BoardArticle.board_id == board_id)
    db.delete(target_article)
    # board 삭제
    db.delete(table_result)
    db.commit()
    return ApiMessage()


# 5. ArticleList API : 특정 게시판의 게시판 글 목록을 가져옵니다.
@app.route('/api/boards/<int:board_id>', methods=['GET'])
def get_article(board_id):
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        page = 1
        limit = 10

    # 유저가 보는 관점에서 0번부터가 아니기에 1빼줌
    page -= 1

    table_result = db.query(BoardArticle).filter(BoardArticle.board_id == board_id).\
        order_by(BoardArticle.create_datetime).offset(page*limit).limit(limit).all() or list()

    # max page 계산
    table_count = db.query(BoardArticle).filter(BoardArticle.board_id == board_id).count()
    max_pages = int(table_count / limit) + (1 if table_count % limit > 0 else 0)

    return ApiMessage(max_pages=max_pages, result=table_result)

#4. Dashboard APIs
  # 1. RecentBoardArticle API : 모든 게시판에 대해 각각의 게시판의 가장 최근 *n* 개의 게시판 글의 *title* 을 가져옵니다.
  #   (즉, *k* 개의 게시판이 있다면 최대 *k * n* 개의 게시판 글의 *title* 을 반환합니다.)


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        board_limit = int(request.args.get('board_limit', 3))
        article_limit = int(request.args.get('article_limit', 5))
    except ValueError:
        board_limit = 3
        article_limit = 5

    boards_result = db.query(Board).order_by(Board.create_datetime).limit(board_limit).all() or list()
    result = dict()

    for _ in boards_result:
        d = [
            {k: v} for k, v in
            db.query(text("'title'"), BoardArticle.title).filter(BoardArticle.board_id == _.id).\
                order_by(BoardArticle.create_datetime).limit(article_limit).all()
        ]
        result[_.id] = d

    return ApiMessage(result=result)
