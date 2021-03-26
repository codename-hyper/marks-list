from website import auth
from flask import Flask, redirect, render_template, Blueprint, request, flash, session, url_for
from flask_login import current_user, login_required
from . import db
from .models import Users, Marks

view = Blueprint('view', __name__)


@view.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        return render_template('home.html', user=current_user)
    else:
        tenth = request.form.get('tenth')
        inter = request.form.get('inter')
        degree = request.form.get('degree')
        updated_marks = Marks(tenthmarks=tenth,
                              intermarks=inter, degreemarks=degree, user_id=current_user.id)
        user = Marks.query.filter_by(user_id=current_user.id).first()
        if user:
            if degree:
                user.degreemarks = degree
            if inter:
                user.intermarks = inter
            if tenth:
                user.tenthmarks = tenth
            db.session.commit()
        else:
            db.session.add(updated_marks)
            db.session.commit()
        flash('Marks updated', category='success')
        return redirect(url_for('view.marks'))


@view.route('/marks', methods=['GET', 'POST'])
@login_required
def marks():
    if request.method == 'GET':
        user_marks = Marks.query.filter_by(user_id=current_user.id).first()
        if user_marks:
            return render_template('marks.html', user=current_user, inter=user_marks.intermarks, degree=user_marks.degreemarks, tenth=user_marks.tenthmarks)
        else:
            flash('Marks not found')
            return redirect(url_for('view.home'))
