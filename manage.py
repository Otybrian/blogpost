from flask_script import Manager, Server
from app import db, create_app
from app.models import User
from flask_migrate import MigrateCommand, Migrate

app = create_app()

manager =  Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
manager.add_command('run',Server(use_debugger=True))

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User)



if __name__ == '__main__':
    manager.run()
