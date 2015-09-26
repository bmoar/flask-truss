from nose.tools import assert_raises
from sqlalchemy.exc import IntegrityError
from flask.ext.testing import TestCase

from flask_truss.factory import create_app
from flask_truss.conf.app import Config
from flask_truss.models.base import db


class LocalhostProxyHack(object):
    """Ensures that a remote_addr is available for testing.
    From http://stackoverflow.com/questions/14872829/get-ip-address-when-testing-flask-application-through-nosetests
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['REMOTE_ADDR'] = environ.get('REMOTE_ADDR', '127.0.0.1')
        return self.app(environ, start_response)


class BaseTestCase(TestCase):
    def create_app(self):
        config = Config()
        app = create_app(config)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.wsgi_app = LocalhostProxyHack(app.wsgi_app)
        test_client = app.test_client()
        app.post = test_client.post
        app.get = test_client.get
        return app

    def setUp(self):
        """Create the testing database, then swap commit for flush"""
        db.create_all()
        self.orig_commit = db.session.commit
        db.session.commit = db.session.flush

    def tearDown(self):
        """Clean up session, sway flush for commit, drop the testing database"""
        db.session.remove()
        db.session.commit = self.orig_commit
        db.drop_all()

    def add_to_session_and_flush_expecting_exception(self, obj):
        db.session.add(obj)
        assert_raises(IntegrityError, db.session.flush)
        db.session.rollback()

    def add_to_session_and_flush(self, obj):
        db.session.add(obj)
        db.session.flush()
