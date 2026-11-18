import json
import uuid
import datetime
import decimal

from flask.json.provider import DefaultJSONProvider


class JSONExtendProvider(DefaultJSONProvider):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, bytes):
            return o.decode('utf-8')
        elif isinstance(o, uuid.UUID):
            return str(o)
        return super().default(o)


class JSONExtendEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, bytes):
            return o.decode('utf-8')
        elif isinstance(o, uuid.UUID):
            return str(o)
        return super().default(o)


# json to dict
def from_json(data):
    return json.loads(data)


# dict to json
def to_json(data):
    return json.dumps(data, cls=JSONExtendEncoder, ensure_ascii=False)
