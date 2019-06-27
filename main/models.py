from datetime import datetime

from app import db


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Article> %r' % self.title


game_users = db.Table(
    'game_users',
    db.Column('game_id', db.ForeignKey('games.id'), primary_key=True),
    db.Column('user_id', db.ForeignKey('users.id'), primary_key=True)
)

# room_users = db.Table(
#     'room_users',
#     db.Column('room_id', db.ForeignKey('rooms.id'), primary_key=True),
#     db.Column('user_id', db.ForeignKey('users.id'), primary_key=True)
# )


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, index=True, unique=True)
    email = db.Column(db.String(40), nullable=True, unique=True)
    password = db.Column(db.String(256), nullable=False)
    submission_data = db.Column(db.DateTime, default=datetime.now())
    update_data = db.Column(db.DateTime, default=datetime.now())
    games = db.relationship(
        'Game',
        secondary=game_users,
        back_populates='users'
    )
    # rooms = db.relationship(
    #     'Room',
    #     secondary=room_users,
    #     back_populates='users'
    # )

    def __repr__(self):
        return '<User> %r' % self.name


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    suit = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    game = db.relationship('Game', backref=db.backref('cards', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cards', lazy=True))

    def __repr__(self):
        return '<Card> %r%r' % (self.suit, self.value)


class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=9)
    small_blind = db.Column(db.Integer, nullable=False, default=2)
    buy_in = db.Column(db.Integer, nullable=False, default=400)
    is_close = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(6))
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin = db.relationship('User', backref=db.backref('rooms', lazy=True))
    # users = db.relationship(
    #     'User',
    #     secondary=room_users,
    #     back_populates='rooms'
    # )

    def __repr__(self):
        return '<Room> %r' % self.title


class Seat(db.Model):
    __tablename__ = 'seats'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy=True))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    room = db.relationship('Room', backref=db.backref('rooms', lazy=True))
    seat = db.Column(db.Integer, nullable=False, default=99)


class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round = db.Column(db.Integer, nullable=False, default=99)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    room = db.relationship('Room', backref=db.backref('games', lazy=True))
    users = db.relationship(
        'User',
        secondary=game_users,
        back_populates='games'
    )

    def __repr__(self):
        return '<Game> %r' % self.id


class Pool(db.Model):
    __tablename__ = 'pools'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chips = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    game = db.relationship('Game', backref=db.backref('pools', lazy=True))

    def __repr__(self):
        return '<Pool> %r' % self.id


if __name__ == '__main__':
    db.create_all()

