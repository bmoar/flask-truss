import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    def __init__(self):
        # Important
        self.SECRET_KEY = 'flask_truss secret key'
        self.CSRF_ENABLED = True

        # Environment settings, mostly used for local development
        self.HOST = 'localhost'
        self.PORT = 5000
        self.DEBUG = True
        self.TESTING = False
        self.THREADED = False

        # logging and performance
        self.MODULE_NAME = __name__.split('.', 1)[0]
        self.LOGGER_NAME = 'debug'
        self.LOGGER_SYSLOGTAG = self.MODULE_NAME.upper()
        self.STATSD_HOST = 'localhost'
        self.STATSD_PORT = 8125

        # SQLAlchemy settings
        self.SQLALCHEMY_RECORD_QUERIES = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True
        self.SQLALCHEMY_ECHO = False
        self.SQLALCHEMY_COMMIT_ON_TEARDOWN = True
        self.SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@host/database'

        # self.SQLALCHEMY_BINDS = {
        #     'secondary': 'postgresql://user:password@host/database'
        # }

        # Celery settings
        self.BROKER_URL = 'amqp://user:password@host/'
        self.CELERY_IMPORTS = ('flask_truss.async._task', )
        self.CELERY_TASK_SERIALIZER = 'json'
        self.CELERY_RESULT_SERIALIZER = 'json'
        self.CELERY_ACCEPT_CONTENT = ['json']
        self.CELERY_ENABLE_UTC = False
        self.BROKER_FAILOVER_STRATEGY = 'round-robin'

        # Flask Debugger Toolbar settings
        self.DEBUG_TB_INTERCEPT_REDIRECTS = False

        self._get_config()

    def _get_config(self):
        """ load config from file, then load envvars.
            hierarchy is:
                envvars
                flat file
                object attr defaults
            with envvars being the highest precedence and object attr defaults the lowest.
            Credit to bmoar
        """
        import configparser
        import ast

        # if the module is called foo.bar.baz, module_name = foo
        module_name = __name__.split('.', 1)[0]

        config = configparser.ConfigParser()
        did_read = config.read('/etc/{0}/{0}.conf'.format(module_name))

        if did_read:
            for section in config.sections():
                for k, v in config.items(section):
                    self.__dict__[k.upper()] = ast.literal_eval(v)

        # add env vars by doing FLASK_TRUSS_{config_opt}
        for k, v in self.__dict__.items():
            envvar = os.environ.get('{0}_{1}'.format(module_name.upper(), k), None)
            if envvar:
                self.__dict__[k.upper()] = envvar

    @staticmethod
    def init_app(app):
        pass
