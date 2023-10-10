from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def bot_echo(msg: Message):
    bot.reply_to(msg, "Enter error.\nIn case you need help: \\help")
