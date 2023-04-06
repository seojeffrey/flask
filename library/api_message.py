from flask import jsonify

from const.response_code import ResponseCode


def ApiMessage(result_code=ResponseCode.OK, **kwargs):
    params = dict()
    if result_code and isinstance(result_code, ResponseCode):
        params["result_code"] = result_code.value
        params["result_message"] = str(result_code)

        params.update(kwargs)

    return jsonify(params)
