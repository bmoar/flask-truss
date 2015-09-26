from marshmallow_sqlalchemy import ModelSchema
from flask_truss.marshmallow import marshmallow

from flask_truss.models.user import User


class SomeSchema(marshmallow.Schema):
    class Meta:
        fields = ('id', 'data')


class UserSchema(ModelSchema):
    class Meta:
        model = User


some_schema = SomeSchema()
somes_schema = SomeSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
