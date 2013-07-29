from flask import Flask, render_template, flash, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, login_required, logout_user
from flask.ext.bootstrap import Bootstrap

__author__ = 'netoho'

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.__init__(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

Bootstrap(app)

from app.admins.models import Admin
from app.admins.forms import LoginForm


@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data, password=form.password.data).first()
        if admin is not None:
            login_user(admin, remember=form.remember_me.data)
            flash('Welcome')
            return redirect(request.args.get("next") or url_for('posts.list_posts'))
        else:
            flash('Username or password incorrect')
            return render_template('login.html', title='Sign In',
                                   form=form)
    return render_template('login.html', title='Sign In',
                           form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Good Bye')
    return redirect(url_for('posts.list_posts'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', title='NetoBlog')


from app.posts.views import mod as postModule
from app.tags.views import mod as tagsModule
from app.admins.views import mod as adminsModule

app.register_blueprint(postModule)
app.register_blueprint(tagsModule)
app.register_blueprint(adminsModule)
