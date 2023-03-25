from random import randint

from config import Config
from monopoly.database.dao import CardDAO, GameDAO, PlayerDAO
from monopoly.database.models import Card, Player
from monopoly.game.card import buy_card
from monopoly.game.player import charge_rent, make_payments, move_player, move_to_prison


def _roll_the_dice() -> int:
    return randint(Config.MIN_DICE_VALUE, Config.MAX_DICE_VALUE)


def _on_roll_dice() -> tuple[int, int, bool]:
    first_roll = _roll_the_dice()
    second_roll = _roll_the_dice()
    return first_roll, second_roll, first_roll == second_roll


def _process_cards_without_cost(player: Player, card: Card) -> str:
    if card.title == Config.LUXURY_TAX_FIELD:
        is_successful = make_payments(player, Config.LUXURY_TAX)
        if is_successful is False:
            PlayerDAO.mark_the_bankrupt(player)
            return f'Player {player.id} lost :('
        return f'Player {player.id} landed on Luxury Tax and has been fined ${Config.LUXURY_TAX}'

    if card.title == Config.INCOME_TAX_FIELD:
        is_successful = make_payments(player, Config.INCOME_TAX)
        if is_successful is False:
            PlayerDAO.mark_the_bankrupt(player)
            return f'Player {player.id} lost :('
        return f'Player {player.id} landed on Income Tax and has been fined ${Config.INCOME_TAX}'

    if card.title == Config.JAIL_FIELD:
        move_to_prison(player)
        return f'Player {player.id} landed on Go to Jail and has been arrested'

    return f'Player {player.id} landed on {card.title}'


def _process_new_card(game_id: str, player: Player, card: Card) -> str:
    was_bought = buy_card(game_id, card, player)
    if was_bought is True:
        return f'Player {player.id} bought {card.title} possessions for the amount of {card.cost}'
    return f'There is not enough money in player {player.id} account to buy {card.title}'


def _check_position(game_id: str, player: Player) -> str:
    card = CardDAO.get_or_create(id=player.position)
    if card.cost is None:
        msg = _process_cards_without_cost(player, card)
        return msg

    possession = GameDAO.get(id=game_id, card_id=card.id)
    if not possession:
        msg = _process_new_card(game_id, player, card)
        return msg

    if possession.player_id == player.id:
        return f'Player {player.id} landed on {card.title}, a possession he/she owns'

    owner = GameDAO.get_or_create(card_id=card.id).player
    is_successful = charge_rent(player, owner, card)
    if is_successful is False:
        PlayerDAO.mark_the_bankrupt(player)
        return f'Player {player.id} lost :('

    return f'Player {player.id} landed on {card.title}, a possession owned by {owner.id}'


def _try_to_get_free(player: Player) -> bool:
    for _ in range(Config.ATTEMPT_TO_GET_FREE):
        _, _, is_double = _on_roll_dice()
        if is_double is True:
            return True

    was_paid = make_payments(player, Config.PRISON_TAX)
    return was_paid


def make_move(game_id: str, player_id: str) -> tuple[int | None, int | None, str]:
    player = PlayerDAO.get_or_create(id=player_id)
    if player.position == Config.PRISON_POSITION:
        if _try_to_get_free(player) is False:
            return None, None, f'Player {player.id} could not be released from jail'

    first_point, second_point, _ = _on_roll_dice()
    move_player(player, first_point + second_point)
    move_result_msg = _check_position(game_id, player)
    return first_point, second_point, f'Player {player_id} got {first_point + second_point} points. {move_result_msg}'
