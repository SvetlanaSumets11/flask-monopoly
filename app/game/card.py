from app.database.dao import GameDAO, PlayerDAO
from app.database.models import Card, Player
from app.game.player import make_payments
from config import Config


def buy_card(game_id: str, card: Card, player: Player) -> bool:
    if player.balance < card.cost:
        return False

    GameDAO.get_or_create(id=game_id, player_id=player.id, card_id=card.id)
    make_payments(player, card.cost)

    if card.color == Config.RAILROAD_COLOR_GROUP:
        PlayerDAO.buy_railroad(player)

    return True
