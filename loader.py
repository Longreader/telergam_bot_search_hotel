from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config
from database import sql

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)

connection = sql.create_connection(config.DB_HOST_NAME)
sql.create_request_table(connection)
