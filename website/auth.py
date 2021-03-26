from flask import Flask, render_template, Blueprint, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Users, Marks
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', user=current_user)
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('login successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.home'))
            else:
                flash('password is wrong, please try again', category='error')
                return render_template('index.html', user=current_user)
        else:
            flash('User not found, please signup', category='error')
            return redirect(url_for('auth.signup'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html', user=current_user)
    else:
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = Users.query.filter_by(email=email).first()
        if user:
            flash('User already signed up, please login', category='error')
            return redirect(url_for('auth.index'))
        else:
            if password1 == password2:
                user = Users(firstname=firstname, lastname=lastname,
                             email=email, password=generate_password_hash(password1, method='sha256'))
                db.session.add(user)
                db.session.commit()
                flash('User signed up successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.home'))
            else:
                flash('somthing went wrong', category='error')
                return redirect(url_for('auth.index'))


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))


@auth.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    user = Users.query.filter_by(id=current_user.id).first()
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Account deleted successfully', category='success')
    return redirect(url_for('auth.index'))
