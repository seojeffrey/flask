import datetime
from flask.json import JSONEncoder

from library.custom_model import EasyModel


class AlchemyEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, EasyModel):
            return o.as_dict()
        if type(o) == datetime.timedelta:
            return str(o)
        if type(o) == datetime.datetime:
            return o.isoformat()
        return super().default(o)

