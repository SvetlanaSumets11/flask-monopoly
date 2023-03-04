from environs import Env

env = Env()
env.read_env('.env')


class Config:
    SECRET_KEY = env('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = env('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REDIS_HOST = env('REDIS_HOST')
    REDIS_PORT = env('REDIS_PORT')
    REDIS_MOVES_LIST = 'moves'

    PRISON_POSITION = 10
    NUM_CARDS_ON_FIELD = 36

    RAILROAD_COLOR_GROUP = 'Railroad'
    LUXURY_TAX_FIELD = 'Luxury Tax'
    INCOME_TAX_FIELD = 'Income Tax'
    JAIL_FIELD = 'Go to Jail'

    RAILROAD_TAX = 25
    PRISON_TAX = 50
    LUXURY_TAX = 75
    INCOME_TAX = 200

    MIN_DICE_VALUE = 1
    MAX_DICE_VALUE = 6

    ATTEMPT_TO_GET_FREE = 2
