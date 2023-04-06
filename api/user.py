# -*- coding: utf-8 -*-
from flask import session, request, redirect, escape, render_template
from app import app
from const.response_code import ResponseCode
from library.api_message import ApiMessage
from model import db
from model.model import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    if 'email' in session:
        return 'Logged in as %s' % escape(session['email'])

    return redirect('/login')


"""
1. User APIs : 유저 SignUp / Login / Logout
"""


# 1. SignUp API : *fullname*, *email*, *password* 을 입력받아 새로운 유저를 가입시킵니다.
@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        params = request.get_json()
        if not params:
            params = request.form
        email = params['email']
        fullname = params['fullname']
        password = params['password']
        re_password = params['re_password']

        if password != re_password:
            return ApiMessage(ResponseCode.THE_TWO_PASSWORD_DO_NOT_MATCHED)
        else:
            if db.query(db.query(User).filter(User.email == email).exists()).scalar():
                return ApiMessage(ResponseCode.EMAIL_EXISTS)

            user = User(email=email, fullname=fullname, password=generate_password_hash(password))
            db.add(user)
            db.commit()

    return ApiMessage()


# ex). check_email API : *email*, 새로 등록 할 수 있는 메일인지 확인
@app.route('/check-email', methods=['POST'])
def check_email():
    params = request.get_json()
    if not params:
        params = request.form
    email = params.get('email')
    if not email:
        return ApiMessage(ResponseCode.CHECK_YOUR_EMAIL)
    if db.query(db.query(User).filter(User.email == email).exists()).scalar():
        return ApiMessage(ResponseCode.EMAIL_EXISTS)
    else:
        return ApiMessage()


# 2. Login API : *email*, *password* 를 입력받아 특정 유저로 로그인합니다.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        params = request.get_json()
        if not params:
            params = request.form
        email = params['email']
        password = params['password']

        user = db.query(User).filter(User.email == email).first()
        if not check_password_hash(user.password, password):
            return ApiMessage(ResponseCode.CHECK_YOUR_PASSWORD_OR_EMAIL)
        else:
            session['email'] = params['email']
            return ApiMessage()


# 3. Logout API : 현재 로그인 된 유저를 로그아웃합니다.
@app.route('/logout')
def logout():
    session.pop('email', None)
    # return redirect('/')
    return ApiMessage()
