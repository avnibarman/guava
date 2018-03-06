import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import application, db, config

# from app import app, db


application.config.from_object(config)

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
