from flask import Blueprint, render_template, current_app, request

from flask_truss.async._task import _task
from flask_truss.lib.logger import flask_endpoint


_blueprint = Blueprint('_blueprint', __name__, template_folder='templates')

@_blueprint.route('/')
@flask_endpoint(log_percent=0.10)
def render_blueprint():
    # Call _task.delay() or _task.apply_async(...) if you've set up a broker.
    _task()
    return render_template('_blueprint.j2', content=None)
