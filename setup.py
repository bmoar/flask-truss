#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='flask_truss',
    version='0.0.1',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    package_data={
        'templates': 'flask_truss/templates/*',
        'static': 'flask_truss/static/*',
        'scripts': 'flask_truss/scripts/migrations/*'
    },
    install_requires=[
        'celery',
        'coverage',
        'Flask-Admin',
        'Flask-Debugtoolbar',
        'Flask-Login',
        'Flask-Marshmallow',
        'Flask-Migrate',
        'Flask-Script',
        'Flask-SQLAlchemy',
        'Flask-Testing',
        'Flask-WTF',
        'Flask',
        'ipdb',
        'ipython',
        'marshmallow-sqlalchemy',
        'nose',
        'paramiko',
        'passlib',
        'psycopg2',
        'python-dateutil',
        'pytz',
        'randomize',
        'SQLAlchemy',
        'statsd',
        'Werkzeug',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
    classifiers=[
        'Private :: Do Not Upload'
    ],
    entry_points={
        'console_scripts': [
            'manage = flask_truss.scripts.manage:main_manager',
            'app = flask_truss.scripts.manage:main_app',
        ]
    }
)
