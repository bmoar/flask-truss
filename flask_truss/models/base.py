from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    created_date = db.Column(db.DateTime, server_default=func.timezone('UTC', func.current_timestamp()))
    modified_date = db.Column(db.DateTime, onupdate=func.timezone('UTC', func.current_timestamp()))

    def save(self):
        """Adds the object to the session and commits the transaction"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes the object and commits the transaction"""
        db.session.delete(self)
        db.session.commit()
