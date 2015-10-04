import os
import time
import statsd
from random import randint
from functools import wraps

from flask import current_app, request


class SyslogtagFilter(object):
    """Injects a syslogtag into a log format"""

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


def is_logged(log_percent=1):
    return True if randint(0, 100) < (100 * log_percent) else False


def flask_endpoint(log_percent=1.00, is_active=True):
    """log a flask endpoint

    :param: :log_percent - what % of requests we want to log, 1.00 = 100%, 0.10 = 10%

    When in debug mode, we log the flask request received, exec time of endpoint
    """

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if is_active and is_logged(log_percent):
                # statsd first to ensure we get a hit ping
                sdclient = statsd.StatsClient(
                    current_app.config['STATSD_HOST'],
                    current_app.config['STATSD_PORT'])
                prefix = '{0}.stats.endpoint.{1}'.format(current_app.config['MODULE_NAME'], func.__qualname__)
                sdclient.incr('{0}.hits'.format(prefix))
                # generate log message for syslog
                log_msg = '''\
    pid="{0}",
    request="{1}",
    url="{2}",
    endpoint="{3}",
    func="{4}",
    data="{5}",
    method="{6}",
    headers="{7}",
    cookies="{8}",
    values="{9}",
    files="{10}",
        '''.format(os.getpid(),
                   hex(id(request)),
                   request.url,
                   request.endpoint,
                   func.__qualname__,
                   request.data,
                   request.method,
                   request.headers,
                   request.cookies,
                   request.values,
                   request.files)

                # performance timing
                time_start = time.perf_counter()
                result = func(*args, **kwargs)
                time_end = time.perf_counter()
                timing = time_end - time_start

                # log timing results
                current_app.logger.info(log_msg + 'exec_time="{0}"'.format(timing))
                sdclient.timing('{0}.exec_time'.format(prefix), timing)

                return result
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorate
