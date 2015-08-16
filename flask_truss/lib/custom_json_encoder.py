import datetime
from decimal import Decimal
from flask.ext.jsontools import DynamicJSONEncoder


class CustomJSONEncoder(DynamicJSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time,)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return obj.total_seconds()
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, list) and not len(obj):
            return []
        else:
            return super().default(obj)
