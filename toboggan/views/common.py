from flask import render_template, redirect, url_for, request, Blueprint, send_file
from toboggan import db, login_manager
from toboggan.models import Dispatcher
from flask_login import UserMixin, login_required, login_user, logout_user, current_user
import bcrypt

common = Blueprint('common', __name__)

context = {
    "current_user": current_user,
    "error": "",
    "dispatcher": Dispatcher
}

@common.route("/")
def main():
    global context
    if len(Dispatcher.query.all()) == 0:
        return redirect(url_for('common.create_user'))
    return render_template('index.html', **context)


@common.route("/login")
@common.route("/login.html")
def login():
    return render_template("login.html", **context)


@common.route("/logout")
@common.route("/logout.html")
def logout():
    logout_user()
    return redirect(url_for('common.main'))


@common.route("/login_user", methods=["POST", "GET"])
def user_login():
    global context
    err_msg = ""
    if request.method == "POST":
        users = Dispatcher.query.filter_by(
            name=request.form['username']
        )
        if users.count() == 1:
            user_id = users[0].id
            user = User(user_id)
            if user.auth_user(users[0].password, request.form['password']):
                login_user(user)

            else:
                err_msg = ('red', "Username/Password combination not valid.")
        else:
            err_msg = ('red', "Username/Password combination not valid.")

    context['current_user'] = current_user
    if len(err_msg):
        context['error'] = err_msg
        return render_template("login.html", **context)
    else:
        return redirect(url_for('common.main'))


@common.route("/create_user")
@common.route("/create_user.html")
def create_user():
    return render_template("create_user.html", **context)


@common.route("/create_first_user", methods=['POST'])
def create_first_user():
    global context
    username = request.form['username']
    if Dispatcher.query.filter_by(name=username).first() is not None:
        err_msg = (
            'red',
            "Account already exists for '{}'.".format(username)
        )
    else:
        if request.form['password'] != request.form['passwordconf']:
            context['error'] = ('red', 'Passwords do not match')
            return render_template('create_user.html', **context)
        password = bcrypt.hashpw(
            request.form['password'].encode(),
            bcrypt.gensalt()
        )
        d = Dispatcher(name=username, password=password)
        db.session.add(d)
        db.session.commit()

        err_msg = ('green', 'Account Created')

    context['error'] = ('green', 'Account Created. Please login')
    return render_template('login.html', **context)

@common.route("/add_user", methods=["POST"])
@login_required
def add_user():
    global context
    username = request.form['username']
    if Dispatcher.query.filter_by(name=username).first() is not None:
        err_msg = (
            'red',
            "Account already exists for '{}'.".format(username)
        )
    else:
        if request.form['password'] != request.form['passwordconf']:
            context['error'] = ('red', 'Passwords do not match')
            return render_template('create_user.html', **context)
        password = bcrypt.hashpw(
            request.form['password'].encode(),
            bcrypt.gensalt()
        )
        d = Dispatcher(name=username, password=password)
        db.session.add(d)
        db.session.commit()

        err_msg = ('green', 'Account Created')

    context['error'] = err_msg
    return render_template('create_user.html', **context)

# User Auth
class User(UserMixin):
    def __init__(self, uid):
        self.id = uid
        first_db_name = Dispatcher.query.filter_by(id=self.id).first()
        self.name = first_db_name.name if first_db_name else None
        self.auth_check = False

    def auth_user(self, db_pwd, form_pwd):
        # Check password
        self.auth_check = db_pwd.encode() == \
            bcrypt.hashpw(
                form_pwd.encode(),
                db_pwd.encode()
            )
        return self.auth_check

    @classmethod
    def get(cls,id):
        return cls.Dispatcher.get(id)

# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)
