from flask import Blueprint, render_template


_blueprint = Blueprint('_blueprint', __name__, template_folder='templates')


@_blueprint.route('/')
def render_blueprint():
    return render_template('_blueprint.j2', content=None)
