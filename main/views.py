from flask import render_template, url_for, redirect, session, g
from werkzeug.security import generate_password_hash
from . import main
from .models import User
from app import db
import pymysql
pymysql.install_as_MySQLdb()


@main.route('/')
def index():
    try:
        # db.drop_all()
        # session.clear()
        # db.create_all()

        # try:
        #     db.create_all()
        if not User.query.all():
            try:
                flop = User(name='flop', password=generate_password_hash('123'))
                turn = User(name='turn', password=generate_password_hash('123'))
                river = User(name='river', password=generate_password_hash('123'))
                db.session.add_all([flop, turn, river])
                db.session.commit()
                return 'ok'
            except Exception as e:
                print(e)
            # except Exception as e:
        #     print(e)
        return 'ok2'
    except Exception as e:
        print(e)




    # if g.user:
    #     return 'blueprint for main.views.index() user_id is :%r' % g.user
    # else:
    #     return '没有session记录'
