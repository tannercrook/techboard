# manager/__init__.py

from flask import Flask, render_template, flash, redirect, request, abort
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .views.auth import auth
from .views.public import public
from .views.manage import manage
from .models.User import User
import sys
import platform

sys.path.append('/var/www/techBoard/techBoard')

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xfc\x123\xda\x06\xc8o\xf3\x95\x01\xafaU\\\xc1Z\xa4\xa9C\xddo\x020]'

# Initialize Bootstrap
bootstrap = Bootstrap(app)

# Initialize Blueprints
app.register_blueprint(auth)
app.register_blueprint(public)
app.register_blueprint(manage)


# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user.get(user_id)


# Default routes

@app.route('/test')
def main():
    return '<h1>Python Version: {}   Path:{}</h1>'.format(platform.python_version(),sys.path)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1>"


