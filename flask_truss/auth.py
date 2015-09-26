from flask_truss.models.user import User
from passlib.hash import bcrypt


def attempt_logon(attempted_name, attempted_password):
    """Attempt to login the user and return a matching user model instance if successful"""
    user = User.query.filter(User.user_name == attempted_name).first()
    try:
        if bcrypt.verify(attempted_password, user.password):
            return user
        else:
            return None
    except (ValueError, AttributeError):
        return None
