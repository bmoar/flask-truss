# flask-truss

Another Flask boilerplate/template application.

##Requirements and assumptions
1. Python 3.4 or greater
1. You probably need a user model, because
1. You are using a database, preferably something compatible with psycopg2

##Installation
1. Clone repo
1. Find and replace flask_truss with appname
1. Find and replace FLASK_TRUSS with APPNAME
1. Create a virtualenv and activate it
1. Run `python setup.py develop`
1. Change directory into appname
1. Start the app with `python manage.py runserver`

##Configuration
Configuration should be done in one of two ways:

1. Environmental variables in the form of `APPNAME_VARIABLE`, matching those in appname/appname/conf/app.py.
2. A file at /etc/appname/appname.conf with the required config in a similar form.

##Running
Run `python manage.py` to get the list of available commands. Run `python manage.py command --help` for further
information about the command and arguments.

##Migrations
Run `python manage.py db init` and manage your schema sanely. See the
[Flask-Migrate](https://flask-migrate.readthedocs.org/en/latest/) docs and the 
[Alembic](https://alembic.readthedocs.org/en/latest/) docs.

##Celery
Run `python manage.py worker` for a simple worker to consume off the queue.

##Admin interface
By default, navigate to `localhost:5000/admin`. See appname/appname/admin.py for how to add models.

##Notes
This boilerplate is by no means complete. I've included an example start of a blueprint, a user model, and a celery
task, but they are by no means the only or the best ways of doing those three things.

Pull requests, issues, and comments are always welcome.
