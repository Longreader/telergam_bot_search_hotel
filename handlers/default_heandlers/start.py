from loader import bot

from telebot import types


@bot.message_handler(commands=['start'])
def bot_start(msg: types.Message):
    bot.delete_state(msg.chat.id, msg.chat.id)
    bot.send_message(msg.chat.id, f"Welcome, {msg.from_user.username}", reply_markup=types.ReplyKeyboardRemove())

