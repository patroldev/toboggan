from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin

# Anon user class
class AnonUser(AnonymousUserMixin):
    def __init__(self):
        self.id = -1
        self.name = None

app = Flask(__name__)

app.config.from_object('config.BaseConfiguration')

db = SQLAlchemy(app)


# Init Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "common.login"
login_manager.anonymous_user = AnonUser


from views.common import common
app.register_blueprint(common)

from toboggan import models
