#!/usr/bin/env python3

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


from flask_truss.factory import create_app
from flask_truss.conf.app import Config
from flask_truss.async.base import celery_instance
from flask_truss.models.base import db


config = Config()
app = create_app(config)
manager = Manager(app)
migrate = Migrate(app, db)


@manager.shell
def make_shell_context():
    """IPython session with app loaded"""
    return dict(app=app)


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
    celery_worker = celery_instance.Worker(queues=queues, concurrency=concurrency, loglevel=loglevel, **app.config)
    celery_worker.start()


manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
