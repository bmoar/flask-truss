from nose.tools import assert_raises
from sqlalchemy.exc import IntegrityError
from flask.ext.testing import TestCase

from flask_truss.factory import create_app
from flask_truss.conf.app import Config
from flask_truss.models.base import db


class BaseTestCase(TestCase):
    def create_app(self):
        config = Config()
        app = create_app(config)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        test_client = app.test_client()
        app.post = test_client.post
        app.get = test_client.get
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_to_session_and_flush_expecting_exception(self, obj):
        db.session.add(obj)
        assert_raises(IntegrityError, db.session.flush)
        db.session.rollback()

    def add_to_session_and_flush(self, obj):
        db.session.add(obj)
        db.session.flush()
