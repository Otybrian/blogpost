from flask_login import login_user, logout_user,login_required
from app.auth import auth
from flask import render_template,flash, request, redirect, url_for
from app.models import User
from .forms import RegistrationForm,LoginForm
from ..email import mail_message

@auth.route('/login',methods = ['POST','GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username = login_form.username.data).first()
        if user != None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('You either entered a wrong password or username')
    return render_template('auth/login.html',login_form = login_form)


@auth.route('/register',methods = ["POST","GET"])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user = User(username=registration_form.username.data, email = registration_form.email.data, password=registration_form.password.data)
        user.save()
        mail_message("Welcome to Blogpost", 'email/-welcome', user.email,user=user)
        return  redirect(url_for('auth.login'))
    return render_template('auth/register.html',registration_form=registration_form )

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))