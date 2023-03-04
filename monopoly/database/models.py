from monopoly.database.db import db
from sqlalchemy.orm import relationship


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.String(length=256), primary_key=True, nullable=False, doc='Unique user id')
    balance = db.Column(db.Integer, nullable=False, default=10000, doc='Money in the user account')
    position = db.Column(db.Integer, nullable=False, default=1, doc='User point on the field')
    in_prison = db.Column(db.Boolean, nullable=False, default=False, doc='Whether the user is in jail or not')
    amount_of_railroads = db.Column(db.Integer, nullable=False, default=0, doc='The number of railways that the user has purchased')
    is_bankrupt = db.Column(db.Boolean, nullable=False, default=False, doc='Whether the user is bankrupt or not')


class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True, nullable=False, doc='Unique card id in the game')
    title = db.Column(db.String(length=256), nullable=False, doc='The name of the card in the game')
    color = db.Column(db.String(length=256), nullable=True, doc='Group of color cards in the game')
    cost = db.Column(db.Integer, nullable=True, doc='The value of the possessions corresponding to the card')
    rental_price = db.Column(db.Integer, nullable=True, doc='Card possessions rental price')


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.String(length=256), nullable=False, doc='Unique game id corresponding to the room id')
    player_id = db.Column(db.String(length=256), db.ForeignKey('players.id', ondelete='CASCADE'), primary_key=True, nullable=False, doc='Unique user id')
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id', ondelete='CASCADE'), primary_key=True, nullable=False, doc='Unique card id in the game')
    player = relationship('Player')
