from flask_script import Manager
from toboggan import app, db, models

app.config.from_object('config.BaseConfiguration')

manager = Manager(app)


@manager.command
def createdb():
    db.create_all()


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)


if __name__ == "__main__":
    manager.run()
