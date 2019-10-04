# svicars/views/auth.py

from flask import Flask, Blueprint, render_template, flash, redirect, request, abort, url_for, session
from flask_login import LoginManager, login_required, login_user, logout_user 
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, InputRequired, EqualTo
from wtforms.fields.html5 import TelField
from techBoard.models.User import *
from techBoard.models.User import User

import hashlib, uuid

# set blueprint
auth = Blueprint('auth', __name__)



@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User()
        user.username = form.username.data 
        user.password = form.password.data.encode('utf-8')

        if(user.makeUserFromCreds()):
            session['user_id'] = user.userID
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('manage.manageIssues')
            return redirect(next)
        else:
            flash('Invalid username or password. ')
    

    return render_template('site/login.html', form=form)



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(1,64)])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')



