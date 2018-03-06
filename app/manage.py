import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from . import application

# from app import app, db


application.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
