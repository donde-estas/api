import os
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand
from flask_dbseeder import Seeder, SeederCommand

from seeds import PersonSeeder
from app import app, db


# Create objects
seeder = Seeder(app, db)    # Create seeder
migrate = Migrate(app, db)  # Create migrator
manager = Manager(app)      # Create manager

# Add commands
manager.add_command('seed', SeederCommand)
seeder.add_seeds([PersonSeeder])

manager.add_command('db', MigrateCommand)

manager.add_command("runserver", Server(
    host='0.0.0.0', port=os.environ.get('PORT')))


if __name__ == '__main__':
    manager.run()
