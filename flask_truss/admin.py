from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView


from flask_truss.models.base import db
from flask_truss.models.user import User


admin_extension = Admin(name='flask_truss Admin', url='/admin', template_mode='bootstrap3')


admin_extension.add_view(ModelView(User, db.session, category="Models"))
