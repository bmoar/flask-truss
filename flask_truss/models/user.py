from flask.ext.login import AnonymousUserMixin, UserMixin

from flask_truss.models.base import BaseModel, db
from passlib.hash import bcrypt


class Anonymous(AnonymousUserMixin):
    pass


class User(UserMixin, BaseModel):
    # __tablename__ needs to be specified depending on the database, since some eg postgres reserve the word `user`.
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, nullable=False)
    pass_hash = db.Column(db.String(60), nullable=False)

    @property
    def password(self):
        """Return the pass_hash as if it were the password."""
        return self.pass_hash

    @password.setter
    def password(self, new_password):
        """Automatically salt and hash the provided password."""
        self.pass_hash = bcrypt.encrypt(new_password)
