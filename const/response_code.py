from enum import IntEnum


class ResponseCode(IntEnum):

    def __str__(self):
        return self._name_

    OK = 2000
    SESSION_NOT_EXISTS = 4000
    EMAIL_EXISTS = 4001
    THE_TWO_PASSWORD_DO_NOT_MATCHED = 4002
    CHECK_YOUR_PASSWORD_OR_EMAIL = 4003
    CHECK_YOUR_EMAIL = 4004

    BOARD_NOT_EXIST = 4100
    BOARD_NAME_NOT_EXIST = 4101
    BOARD_PERMISSION_DENIED = 4102
    BOARD_ARTICLE_NOT_EXISTS = 4110
    ARTICLE_NO_CONTENTS_OR_TITLE = 4111
    ARTICLE_PERMISSION_DENIED = 4102
