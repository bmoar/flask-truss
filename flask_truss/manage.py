from flask.ext.script import Manager

from flask_truss.factory import create_app
from flask_truss.conf.app import Config
from flask_truss.async.base import celery_instance

config = Config()
app = create_app(config)
manager = Manager(app)


def make_shell_context():
    return dict(app=app)


@manager.shell
def make_shell_context():
    """IPython session with app loaded"""
    return dict(app=app)


@manager.option('-n', '--nose_arguments', dest='nose_arguments', required=False,
                help="List of arguments to pass to nose. First argument MUST be ''",
                default=['', '--with-coverage', '--cover-package=flask_truss'])
def test(nose_arguments):
    """Run nosetests with the given arguments and report coverage"""
    assert nose_arguments[0] == ''
    import nose
    from nose.plugins.cover import Coverage
    nose.main(argv=nose_arguments, addplugins=[Coverage()])


@manager.command
def runserver():
    """Run the Flask development server with the config's settings"""
    app.run(port=config.PORT, debug=config.DEBUG, threaded=config.THREADED)


@manager.option('-Q', '--queues', dest='queues', required=False, default='celery',
                help="Comma separated names of queues")
@manager.option('-c', '--concurrency', dest='concurrency', required=False, type=int, default=0,
                help="Number of processes/threads the worker uses")
@manager.option('-l', '--loglevel', dest='loglevel', required=False, default='INFO',
                help="DEBUG, INFO, WARN, ERROR, CRITICAL, FATAL")
def worker(queues, concurrency, loglevel=None):
    """Run a celery worker process locally"""
    worker = celery_instance.Worker(queues=queues, concurrency=concurrency, loglevel=loglevel, **app.config)
    worker.start()


if __name__ == "__main__":
    manager.run()
