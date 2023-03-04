from monopoly.app import app
from monopoly.socketio_events import socketio

if __name__ == "__main__":
    socketio.run(app)
