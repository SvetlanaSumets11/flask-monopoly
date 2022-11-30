from flask import copy_current_request_context, Flask, render_template, request
from flask_migrate import Migrate
from flask_socketio import disconnect, emit, join_room, leave_room, rooms, SocketIO

from app.database.db import db
from app.database.fill_board import initialize_board
from app.game.game import make_move
from app.game.player import check_balance, check_is_bankrupt, come_out_of_game, start_game_for_player
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

Migrate(app, db)
socketio = SocketIO(app, async_mode=None)


def run_app():
    with app.app_context():
        initialize_board()
    socketio.run(app)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.event
def publish_my_event(message):
    emit('response', {'data': message['data']})


@socketio.event
def publish_broadcast_event(message):
    emit('response', {'data': message['data']}, broadcast=True)


@socketio.event
def join(message):
    join_room(message['room'])
    start_game_for_player(player_id=request.sid)

    balance = check_balance(player_id=request.sid)
    emit('response', {'data': f'You joined the room {message["room"]}. Your balance: {balance}'})
    emit('response', {'data': f'Player {request.sid} joined room {message["room"]}'}, to=message['room'])


@socketio.event
def leave():
    emit('response', {'data': f'You left room {rooms()[-1]}'})
    emit('response', {'data': f'Player {request.sid} left room {rooms()[-1]}'}, to=rooms()[-1])

    come_out_of_game(player_id=request.sid)
    leave_room(rooms()[-1])


@socketio.event
def publish_room_event(message):
    message = f'Player {request.sid} wrote a message {message["data"]} to room {rooms()[-1]}'
    emit('response', {'data': message}, to=rooms()[-1])


@socketio.event
def start():
    result = make_move(game_id=rooms()[-1], player_id=request.sid)
    emit('response', {'data': result}, to=rooms()[-1])
    emit('response', {'data': f'Your balance: {check_balance(request.sid)}'})
    if check_is_bankrupt(request.sid):
        come_out_of_game(player_id=request.sid)
        leave_room(rooms()[-1])


@socketio.event
def make_disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    emit('response', {'data': 'Disconnected'}, callback=can_disconnect)


@socketio.on('disconnect')
def test_disconnect():
    print(f'Client {request.sid} disconnected')


@socketio.event
def connect():
    emit('response', {'data': 'Connected'})
