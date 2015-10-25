from flask_truss.tests.integrations import BaseTestCase
from flask_truss.models.user import User, Anonymous


class TestAnonymousModel(BaseTestCase):
    def test_anonymous(self):
        anon = Anonymous()
        assert anon.is_authenticated is False
        assert anon.is_active is False
        assert anon.is_anonymous is True
        assert anon.get_id() is None
