from functools import wraps
from flask import session
from const.response_code import ResponseCode
from library.api_message import ApiMessage


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return ApiMessage(ResponseCode.SESSION_NOT_EXISTS)
        return f(*args, **kwargs)
    return decorated_function


