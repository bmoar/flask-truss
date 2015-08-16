from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.jsontools import JsonSerializableBase

db = SQLAlchemy()


class BaseModel(db.Model, JsonSerializableBase):
    __abstract__ = True
