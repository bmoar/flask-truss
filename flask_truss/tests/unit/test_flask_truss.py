from flask_truss.tests.unit import BaseTestCase


class TestFlaskTruss(BaseTestCase):
    def test_extensions_get_registered_correctly(self):
        extensions = self.app.extensions.keys()
        print(extensions)
        assert 'admin' in extensions
        assert 'sqlalchemy' in extensions

    def test_blueprints_exist(self):
        blueprints = self.app.blueprints.keys()
        assert '_blueprint' in blueprints

    def test_basic_routes(self):
        rv = self.app.get('/', follow_redirects=False)
        assert rv.status_code == 200
        assert b'None' in rv.data
