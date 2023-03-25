from config import Config
from monopoly.database.dao import GameDAO, PlayerDAO
from monopoly.database.models import Card, Player


def move_player(player: Player, number_on_dice: int):
    PlayerDAO.move_player(player, number_on_dice)


def _replenish_balance(player: Player, amount_of_money: int):
    PlayerDAO.replenish_balance(player, amount_of_money)


def charge_rent(player: Player, owner: Player, card: Card) -> bool:
    if card.color == Config.RAILROAD_COLOR_GROUP:
        rent_amount = Config.RAILROAD_TAX * owner.amount_of_railroads
    else:
        rent_amount = card.rental_price

    was_paid = make_payments(player, rent_amount)
    if was_paid is False:
        return False

    _replenish_balance(owner, rent_amount)
    return True


def make_payments(player: Player, amount: int) -> bool:
    if player.balance < amount:
        return False

    PlayerDAO.make_payments(player, amount)
    return True


def move_to_prison(player: Player):
    PlayerDAO.move_to_imprison(player)


def start_game_for_player(player_id: str):
    PlayerDAO.get_or_create(id=player_id)


def check_balance(player_id: str) -> int:
    balance = PlayerDAO.get(id=player_id).balance
    return balance


def check_is_bankrupt(player_id: str) -> int:
    is_bankrupt = PlayerDAO.get(id=player_id).is_bankrupt
    return is_bankrupt


def come_out_of_game(player_id: str):
    GameDAO.delete_all(player_id=player_id)
    PlayerDAO.delete_all(id=player_id)
