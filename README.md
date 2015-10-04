# flask-truss

Another Flask boilerplate/template application.

##Requirements and assumptions
1. Python 3.4 or greater
1. You probably need a user model, because
1. You are using a database, preferably something compatible with psycopg2

##Included Libraries
The full list can be found in `flask-truss/setup.py`:
1. SQLAlchemy
1. Alembic
1. Marshmallow
1. Passlib
1. Celery
1. WTForms

##Installation
1. Clone repo
1. Find and replace flask_truss and flask-truss with appname (your application's name)
1. Find and replace FLASK_TRUSS with APPNAME
1. Make sure gcc or llvm-gcc is available: run `export CC=/usr/bin/llvm-gcc` or similar if not
1. Create a virtualenv and activate it
1. Run `python setup.py develop`
1. Start the app with `python manage.py runserver`

##Configuration
Configuration should be done in one of two ways:

1. Environmental variables in the form of `APPNAME_VARIABLE`, matching those in `appname/appname/conf/app.py`.
1. A file at `/etc/appname/appname.conf` with the required config in the form:

    ```
    [appname]
    VARIABLE='value'
    OTHER_VARIABLE={'key': 1}
    ```


##Running
Run `python manage.py` to get the list of available commands. Run `python manage.py command --help` for further
information about the command and arguments.

##Migrations
Run `python manage.py db` and manage your database schemas sanely. See the
[Flask-Migrate](https://flask-migrate.readthedocs.org/en/latest/) docs and the 
[Alembic](https://alembic.readthedocs.org/en/latest/) docs.

##Celery
Run `python manage.py worker` for a simple worker to consume off the queue. Read `manage.py` for additional options.

##Admin Interface
By default, navigate to `localhost:5000/admin`. See `appname/appname/admin.py` for how to add models.

##Marshalling
This project sets up [marshmallow](https://marshmallow.readthedocs.org/en/latest/) via [
flask-marshmallow](http://flask-marshmallow.readthedocs.org/en/latest/) and
[marshmallow-sqlalchemy](https://marshmallow-sqlalchemy.readthedocs.org/en/latest/) for marshalling data. See a very
simple example in `appname/appname/schema/user.py`.

##Testing
This project uses nose and unittest. Run all of the tests with `./nosetests.sh`, or specific tests with 
`./nosetests.sh appname/tests/unit/`. Tests are split into unit and integration tests. Unit tests are self-contained
and require no third party interactions. Integration tests rely on configuration, external services, flask, database, or
any other services. By default, this command will run nosetests with coverage and cover-branches.

##Other Useful Bits
1. `appname/appname/lib/logger.py` contains a decorator called `flask_endpoint`, written by @bmoar, that logs a 
percentage of traffic that hits an endpoint.
1. `appname/appname/setup.py` includes two 
[entry points](https://pythonhosted.org/setuptools/setuptools.html#automatic-script-creation)

##Notes
This boilerplate is by no means complete. I've included an example start of a blueprint, a user model, and a celery
task, but they are not the only ways or the best ways of doing those three things.

Pull requests, issues, and comments are always welcome.
