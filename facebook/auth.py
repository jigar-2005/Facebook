from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    elif request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            login_user(user, remember=True)
            user.last_seen = datetime.now()
            db.session.commit()
            flash('Welcome ' + user.firstname + " " + user.lastname, 'success')
            return redirect(url_for('views.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("facebook_login_page.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        dob = request.form.get('dob')
        sex = request.form.get('sex')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', 'error')
            return render_template("facebook_signup_page.html")
        elif password1 != password2:
            flash('Passwords don\'t match.', 'error')
            return render_template("facebook_signup_page.html")
        else:
            new_user = User(firstname=first_name, lastname=last_name, email=email, password=generate_password_hash(
                password1, method='sha256'), date_of_birth=dob, gender=sex)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!, You are now able to log in', 'success')
            return redirect(url_for('auth.login'))
    return render_template("facebook_signup_page.html")
