import os


class SyslogtagFilter(object):
    """ Injects a syslogtag into a log format """

    def __init__(self, syslogtag):
        self.syslogtag = syslogtag

    def filter(self, record):
        record.syslogtag = self.syslogtag
        return True


def init_logger(syslogtag='FLASK_TRUSS', logger_name='stderr'):
    """A smarter syslog logger

    Credit to bmoar
    """
    import logging
    from logging import config

    logger_dict = {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'syslogtag': {
                    '()': SyslogtagFilter,
                    'syslogtag': syslogtag,
                    },
                },
            'formatters': {
                'detailed': {
                    'format': '[%(syslogtag)s] [%(levelname)s] (%(filename)s:%(funcName)s:%(lineno)s) %(message)s'
                    },
                },
            'handlers': {
                'stderr': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stderr',
                    'formatter': 'detailed',
                    'filters': ['syslogtag'],
                    },
                'syslog': {
                    'class': 'logging.handlers.SysLogHandler',
                    'address': '/dev/log' if os.path.exists('/dev/log') else '/var/run/syslog',
                    'formatter': 'detailed',
                    'filters': ['syslogtag'],
                    },
                },
            'loggers': {
                'stderr': {
                    'level': 'INFO',
                    'handlers': ['stderr'],
                    'propagate': False,
                    },
                'stderr_syslog': {
                    'level': 'INFO',
                    'handlers': ['stderr', 'syslog'],
                    'propagate': False,
                    },
                'debug': {
                    'level': 'DEBUG',
                    'handlers': ['stderr'],
                    'propagate': False,
                    },
                'debug_syslog': {
                    'level': 'DEBUG',
                    'handlers': ['stderr', 'syslog'],
                    'propagate': False,
                    },
                'prod': {
                    'level': 'INFO',
                    'handlers': ['syslog'],
                    'propagate': False,
                    },
                'prod_debug': {
                    'level': 'DEBUG',
                    'handlers': ['syslog'],
                    'propagate': False,
                    },
                },
            'root': {
                'level': 'INFO',
                'handlers': ['stderr'],
                },
            }
    logging.config.dictConfig(logger_dict)

    if logger_dict['loggers'][logger_name]['level'] == 'DEBUG':
        logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy').handlers = logging.getLogger(logger_name).handlers

    return logging.getLogger(logger_name)

def log_flask_request(flask_app=None, request=None):
    """ logs a request from a flask app
    :param flask_app: a Flask app object (should be current_app from flask side)
    :param request: the flask request object to log
    """
    flask_app.logger.info('request="{0}", url="{1}"'.format(hex(id(request)), request.url))
    flask_app.logger.info('request="{0}", endpoint="{1}"'.format(hex(id(request)), request.endpoint))
    flask_app.logger.info('request="{0}", data="{1}"'.format(hex(id(request)), request.data))
    flask_app.logger.info('request="{0}", method="{1}"'.format(hex(id(request)), request.method))
    flask_app.logger.info('request="{0}", headers="{1}"'.format(hex(id(request)), request.headers))
    flask_app.logger.info('request="{0}", cookies="{1}"'.format(hex(id(request)), request.cookies))
    flask_app.logger.info('request="{0}", values="{1}"'.format(hex(id(request)), request.values))
    flask_app.logger.info('request="{0}", files="{1}"'.format(hex(id(request)), request.files))
