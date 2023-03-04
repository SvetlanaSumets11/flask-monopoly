from enum import StrEnum

from flask import copy_current_request_context, request
from flask_socketio import disconnect, emit, join_room, leave_room, rooms

from config import Config
from monopoly.app import redis, socketio
from monopoly.game.game import make_move
from monopoly.game.player import check_balance, check_is_bankrupt, come_out_of_game, start_game_for_player


class Event(StrEnum):
    my_event = 'my event'
    broadcast_event = 'broadcast event'
    join = 'join'
    leave = 'leave'
    room_event = 'room event'
    start = 'start'
    disconnect = 'disconnect'
    connect = 'connect'


def _form_response(event: str, user_id: str, data: str, **kwargs) -> tuple[str, dict]:
    result = {'event': event, 'user': user_id, 'message': data} | kwargs
    return 'response', result


def _get_current_room() -> str:
    return rooms()[-1]


def _get_current_player() -> str:
    moves = redis.lrange(Config.REDIS_MOVES_LIST, 0, redis.llen(Config.REDIS_MOVES_LIST) - 1)
    return moves[0]


@socketio.event
def publish_my_event(message: dict):
    emit(*_form_response(Event.my_event, request.sid, message['data']))


@socketio.event
def publish_broadcast_event(message: dict):
    emit(*_form_response(Event.broadcast_event, request.sid, message['data']), broadcast=True)


@socketio.event
def join(message: dict):
    join_room(message['room'])
    start_game_for_player(player_id=request.sid)

    balance = check_balance(player_id=request.sid)
    emit(*_form_response(Event.join, request.sid, f'You joined the room {message["room"]}. Your balance: {balance}'))
    emit(
        *_form_response(Event.join, request.sid, f'Player {request.sid} joined room {message["room"]}'),
        to=message['room'],
    )

    redis.rpush(Config.REDIS_MOVES_LIST, request.sid)


@socketio.event
def leave():
    emit(*_form_response(Event.leave, request.sid, f'You left room {_get_current_room()}'))
    emit(
        *_form_response(Event.leave, request.sid, f'Player {request.sid} left room {_get_current_room()}'),
        to=_get_current_room(),
    )

    come_out_of_game(player_id=request.sid)
    leave_room(_get_current_room())

    redis.lrem(Config.REDIS_MOVES_LIST, 1, request.sid)


@socketio.event
def publish_room_event(message: dict):
    message = f'Player {request.sid} wrote a message {message["data"]} to room {_get_current_room()}'
    emit(*_form_response(Event.room_event, request.sid, message), to=_get_current_room())


@socketio.event
def start():
    current_player = _get_current_player()
    if current_player.decode() != request.sid:
        emit(*_form_response(Event.start, request.sid, f"Now it's not your turn, now it's player {current_player}"))
        return

    first_point, second_point, result = make_move(game_id=_get_current_room(), player_id=request.sid)
    emit(
        *_form_response(Event.start, request.sid, result, first_point=first_point, second_point=second_point),
        to=_get_current_room(),
    )
    emit(*_form_response(Event.start, request.sid, f'Your balance: {check_balance(request.sid)}'))

    redis.lpop(Config.REDIS_MOVES_LIST)
    redis.rpush(Config.REDIS_MOVES_LIST, request.sid)

    if check_is_bankrupt(request.sid):
        come_out_of_game(player_id=request.sid)
        leave_room(_get_current_room())
        redis.lrem(Config.REDIS_MOVES_LIST, 1, request.sid)


@socketio.event
def make_disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()
    emit(*_form_response(Event.disconnect, request.sid, 'Disconnected'), callback=can_disconnect)


@socketio.event
def connect():
    emit(*_form_response(Event.connect, request.sid, 'Connected'))
