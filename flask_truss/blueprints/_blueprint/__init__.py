from flask import Blueprint, render_template, current_app, request

from flask_truss.logger import log_flask_request


_blueprint = Blueprint('_blueprint', __name__, template_folder='templates')


@_blueprint.route('/')
def render_blueprint():
    log_flask_request(current_app, request)
    return render_template('_blueprint.j2', content=None)
