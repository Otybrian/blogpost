from app import db, create_app
from app.models import User, Comment, Post
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager, Server


app = create_app('development')

manager =  Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
manager.add_command('server', Server)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User, Post = Post, Comment=Comment)



if __name__ == '__main__':
    manager.run()
