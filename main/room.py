from flask import request, render_template, url_for, redirect, session, flash, g, jsonify

import random

from . import main
from .auth import login_required
from .models import User, Room, Game, Card, Seat
from app import db
import pymysql
pymysql.install_as_MySQLdb()

from .poker import Poker


@main.route('/create_room', methods=('GET', 'POST'))
@login_required
def create_room():
    if request.method == 'POST':
        title = request.form['room-title']
        sb = request.form['room-sb']
        buyin = request.form['room-buy-in']
        capacity = request.form['room-capacity']
        error = None

        if title is None:
            error = '房间名不能为空。'

        if error is None:
            password = generate_password()
            user_id = g.user.id
            try:
                room = Room(
                    title=title,
                    capacity=capacity,
                    small_blind=sb,
                    buy_in=buyin,
                    password=password,
                    admin_id=user_id
                )
                db.session.add(room)
                db.session.commit()
                g.room = room
                try:
                    seat = Seat(user_id=user_id, room_id=room.id)
                    db.session.add(seat)
                    db.session.commit()
                except Exception as e:
                    print('进入房间出错')
                    print(e)
                return '房间创建成功：room Num is: %d' % password
            except Exception as e:
                error = e
                return '房间创建出错：error is: %r' % error

        flash(error)
    return render_template('room/create-room.html')


@main.route('/join_room', methods=('GET', 'POST'))
@login_required
def join_room():
    if request.method == 'POST':
        password = request.form['room-password']
        room = Room.query.filter_by(password=password).filter_by(is_close=False).first()
        error = None
        if password is None:
            error = '房间号不能为空'
        elif room is None:
            error = '房间不存在'

        if error is None:
            try:
                seat = Seat(user_id=1, room_id=room.id)
                db.session.add(seat)
                db.session.commit()
                return redirect(url_for('.desk'))
            except Exception as e:
                error = '加入房间出错'
                print(error)
                print(e)

        flash(error)

    return render_template('room/join-room.html')


def generate_password():
    password = random.randint(100000, 999999)
    while True:
        if not Room.query.filter_by(password=password).first():
            return password


@main.route('/desk', methods=('GET', 'POST'))
@login_required
def desk():
    room = Room.query.filter_by(user_id=g.user.id).filter_by(is_close=False).first()
    session['room'] = room.id
    game_id = session.get('game')
    button_text = '开始游戏'
    cmd = 0
    player_cards_style = []
    flop_cards = []
    turn_cards = []
    river_cards = []
    if game_id:
        now_game = Game.query.filter_by(id=game_id).first()
        if now_game.round == 0:
            player_cards_style = pre_flop()
            button_text = '继续发牌'
            g.player_cards = player_cards_style
            cmd = 1
        elif now_game.round == 1:
            cmd = 2
            flop_cards = flop()
            button_text = '继续发牌'
        elif now_game.round == 2:
            cmd = 3
            turn_cards = turn()
            button_text = '继续发牌'
        elif now_game.round == 3:
            cmd = 4
            river_cards = river()
            button_text = '重新开始'
        else:
            generate_game()
            player_cards_style = pre_flop()
            button_text = '继续发牌'
            g.player_cards = player_cards_style
            cmd = 1
    return render_template(
        'room/desk.html',
        room=room,
        button_text=button_text,
        player_cards=player_cards_style,
        flop_cards=flop_cards,
        turn_cards=turn_cards,
        river_cards=river_cards,
        cmd=cmd)


@main.route('/_start_game')
def start_game():
    cmd = request.args.get('cmd', 0, type=int)
    button_text = ''
    player_cards_style = []
    flop_cards = []
    turn_cards = []
    river_cards = []
    if cmd == 0 or cmd == 4:
        generate_game()
        player_cards_style = pre_flop()
        button_text = '继续发牌'
        g.player_cards = player_cards_style
        cmd = 1
    elif cmd == 1:
        cmd = 2
        flop_cards = flop()
    elif cmd == 2:
        cmd = 3
        turn_cards = turn()
    elif cmd == 3:
        cmd = 4
        river_cards = river()
        button_text = '重新开始'
    return jsonify(
        result=button_text,
        player_cards=player_cards_style,
        flop_cards=flop_cards,
        turn_cards=turn_cards,
        river_cards=river_cards,
        cmd=cmd)


def generate_game():
    user_id = g.user.id
    room_id = session.get('room')
    user = User.query.filter_by(id=user_id).first()
    try:
        game = Game(round=99, room_id=room_id)
        user.games.append(game)
        db.session.add(game)
        db.session.add(user)
        db.session.commit()
        g.game = game
        session['game'] = game.id
        poker = Poker()
        poker.generate_cards()
        poker.riffle()

        cards = poker.send_card(2)
        for card in cards:
            try:
                card = Card(value=card['value'], suit=card['suit'], game_id=game.id, user_id=user_id)
                db.session.add(card)
                db.session.commit()
            except Exception as e:
                print(e)

        poker.send_card()
        flop_cards = poker.send_card(3)
        for card in flop_cards:
            try:
                flop = User.query.filter_by(name='flop').first()
                card = Card(value=card['value'], suit=card['suit'], game_id=game.id, user_id=flop.id)
                db.session.add(card)
                db.session.commit()
            except Exception as e:
                print(e)

        poker.send_card()
        turn_cards = poker.send_card()
        for card in turn_cards:
            try:
                turn = User.query.filter_by(name='turn').first()
                card = Card(value=card['value'], suit=card['suit'], game_id=game.id, user_id=turn.id)
                db.session.add(card)
                db.session.commit()
            except Exception as e:
                print(e)

        poker.send_card()
        river_cards = poker.send_card()
        for card in river_cards:
            try:
                river = User.query.filter_by(name='river').first()
                card = Card(value=card['value'], suit=card['suit'], game_id=game.id, user_id=river.id)
                db.session.add(card)
                db.session.commit()
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


def pre_flop():
    user_id = g.user.id
    game_id = session.get('game')
    cards = Card.query.filter_by(game_id=game_id).filter_by(user_id=user_id)
    try:
        game_update = Game.query.filter_by(id=game_id).first()
        game_update.round = 0
        db.session.add(game_update)
        db.session.commit()
    except Exception as e:
        print(e)
    player_cards = []
    for card in cards:
        card_dict = {'value': card.value, 'suit': card.suit}
        player_cards.append(card_dict)
    return get_cards_style(player_cards)


def flop():
    game_id = session.get('game')
    flop_id = User.query.filter_by(name='flop').first().id
    cards = Card.query.filter_by(game_id=game_id).filter_by(user_id=flop_id)
    try:
        game_update = Game.query.filter_by(id=game_id).first()
        game_update.round = 1
        db.session.add(game_update)
        db.session.commit()
    except Exception as e:
        print(e)
    flop_cards = []
    for card in cards:
        card_dict = {'value': card.value, 'suit': card.suit}
        flop_cards.append(card_dict)
    return get_cards_style(flop_cards)


def turn():
    game_id = session.get('game')
    turn_id = User.query.filter_by(name='turn').first().id
    cards = Card.query.filter_by(game_id=game_id).filter_by(user_id=turn_id)
    try:
        game_update = Game.query.filter_by(id=game_id).first()
        game_update.round = 2
        db.session.add(game_update)
        db.session.commit()
    except Exception as e:
        print(e)
    turn_cards = []
    for card in cards:
        card_dict = {'value': card.value, 'suit': card.suit}
        turn_cards.append(card_dict)
    return get_cards_style(turn_cards)


def river():
    game_id = session.get('game')
    river_id = User.query.filter_by(name='river').first().id
    cards = Card.query.filter_by(game_id=game_id).filter_by(user_id=river_id)
    try:
        game_update = Game.query.filter_by(id=game_id).first()
        game_update.round = 3
        db.session.add(game_update)
        db.session.commit()
    except Exception as e:
        print(e)
    river_cards = []
    for card in cards:
        card_dict = {'value': card.value, 'suit': card.suit}
        river_cards.append(card_dict)
    return get_cards_style(river_cards)


def get_cards_style(cards):
    card_style = []
    for card in cards:
        card_style.append(get_style(card))
    return card_style


def get_style(card):
    if card['value'] in range(2, 15) and card['suit'] in ['hearts', 'spades', 'diamonds', 'clubs']:
        value_ico = card['suit'] + "-" + str(card['value'])
        suit_ico = card['suit'] + "-small"
        if card['value'] in range(2, 11) or card['value'] == 14:
            suit_image = card['suit'] + "-big"
        else:
            suit_image = card['suit'] + "-big-" + str(card['value'])
        return {'value_ico': value_ico, 'suit_ico': suit_ico, 'suit_image': suit_image}