import os
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("runserver", Server(
    host='0.0.0.0', port=os.environ.get('PORT')))

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
