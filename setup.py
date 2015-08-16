from setuptools import setup, find_packages

setup(
    name='flask_truss',
    version='0.0.1',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    package_data={
        'templates': 'flask_truss/templates/*',
        'static': 'flask_truss/static/*'
    },
    install_requires=[
        'celery',
        'coverage',
        'Flask-Admin',
        'Flask-Bcrypt',
        'Flask-Debugtoolbar',
        'Flask-JSONTools',
        'Flask-Login',
        'Flask-Script',
        'Flask-SQLAlchemy',
        'Flask-Testing',
        'Flask-WTF',
        'Flask',
        'ipdb',
        'ipython',
        'nose',
        'paramiko',
        'psycopg2',
        'py-bcrypt',
        'python-dateutil',
        'pytz',
        'randomize',
        'SQLAlchemy',
        'Werkzeug',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
    classifiers=[
        'Private :: Do Not Upload'
    ]
)
