from flask import request, render_template, url_for, redirect, session, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
import functools

from . import main
from .models import User
from app import db
import pymysql
pymysql.install_as_MySQLdb()


@main.route('/reg', methods=('GET', 'POST'))
def reg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not username:
            error = '用户名不能为空。'
        elif not password:
            error = '密码不能为空。'
        elif User.query.filter_by(name=username).first() is not None:
            error = '用户名 {} 已经存在。'.format(username)
        elif User.query.filter_by(email=email).first() is not None:
            error = '邮箱 {} 已经存在。'.format(email)

        if error is None:
            password = generate_password_hash(password)
            user = User(name=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))

        flash(error)

    return render_template('auth/register.html')


@main.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter_by(name=username).first()

        if username is None:
            error = '用户名不能为空。'
        elif password is None:
            error = '密码不能为空。'
        elif user is None:
            error = '用户名或密码错误 。'
        elif not check_password_hash(user.password, password):
            error = '密码错误。'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.profile'))

        flash(error)

    return render_template('auth/login.html')


def login_required(view):
    """登录状态检查，通过全局g存储user信息进行判断"""
    @functools.wraps(view)
    def wraps_view(**kwargs):
        if g.user is None:
            return redirect(url_for('main.login'))
        return view(**kwargs)
    return wraps_view


@main.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


@main.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))