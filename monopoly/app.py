from flask import Flask
from flask_migrate import Migrate
from flask_socketio import SocketIO
import redis as redis

from config import Config
from monopoly.database.db import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
Migrate(app, db)

redis = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

socketio = SocketIO(app, async_mode=None)

import monopoly.routes  # noqa
import monopoly.socketio_events  # noqa
