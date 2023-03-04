from abc import ABC, abstractmethod
import logging

from sqlalchemy import exc

from config import Config
from monopoly.database.db import db
from monopoly.database.models import Card, Game, Player

logger = logging.getLogger(__name__)


class BaseDAO(ABC):
    @property
    @abstractmethod
    def model(self):
        pass

    @staticmethod
    def _save(instance: db.Model):
        try:
            db.session.add(instance)
            db.session.commit()
        except exc.DatabaseError as e:
            logger.critical(f'Rollback on save, {e}')
            db.session.rollback()

    @staticmethod
    def delete(instance: db.Model):
        try:
            db.session.delete(instance)
            db.session.commit()
        except exc.DatabaseError as e:
            logger.critical(f'Rollback on delete, {e}')
            db.session.rollback()

    @classmethod
    def get_or_create(cls, **kwargs) -> db.Model:
        instance = cls.model.query.filter_by(**kwargs).first()

        if not instance:
            instance = cls.model(**kwargs)
            cls._save(instance)

        return instance

    @classmethod
    def get(cls, **kwargs) -> db.Model:
        instance = cls.model.query.filter_by(**kwargs).first()
        return instance

    @classmethod
    def get_all(cls, **kwargs) -> list[db.Model]:
        instances = cls.model.query.filter_by(**kwargs).all()
        return instances

    @classmethod
    def delete_all(cls, **kwargs):
        cls.model.query.filter_by(**kwargs).delete()
        db.session.commit()


class CardDAO(BaseDAO):
    model = Card


class PlayerDAO(BaseDAO):
    model = Player

    @classmethod
    def buy_railroad(cls, player: Player):
        player.amount_of_railroads += 1
        cls._save(player)

    @classmethod
    def move_player(cls, player: Player, number_on_dice: int):
        player.position = (player.position + number_on_dice - 1) % Config.NUM_CARDS_ON_FIELD + 1
        cls._save(player)

    @classmethod
    def replenish_balance(cls, player: Player, amount_of_money: int):
        player.balance += amount_of_money
        cls._save(player)

    @classmethod
    def make_payments(cls, player: Player, amount: int):
        player.balance -= amount
        cls._save(player)

    @classmethod
    def move_to_imprison(cls, player: Player):
        player.position = Config.PRISON_POSITION
        cls._save(player)

    @classmethod
    def mark_the_bankrupt(cls, player: Player):
        player.is_bankrupt = True
        cls._save(player)


class GameDAO(BaseDAO):
    model = Game
