import os
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

from seeds import PersonSeeder


# Create objects
migrate = Migrate(app, db)  # Create migrator
manager = Manager(app)      # Create manager

# Add commands
manager.add_command('seed', PersonSeeder())

manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server(
    host='0.0.0.0', port=os.environ.get('PORT')))


if __name__ == '__main__':
    manager.run()
