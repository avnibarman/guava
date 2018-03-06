import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import application, db, config

# from app import app, db


application.config.from_object(config)

migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
