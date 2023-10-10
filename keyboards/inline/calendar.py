import datetime

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from loader import bot
from logs.log import log_dec
from telebot import types

from states.SearchHotel import UserSearchState

from handlers.custom_heandlers import hotels_script


@log_dec
def set_date_in(message: types.Message):
    """
    Function call day to check in
    :param message: User message
    """
    text = "Please, select a date of check in"
    bot.send_message(message.chat.id, text)
    date = datetime.date.today()
    calendar, step = DetailedTelegramCalendar(calendar_id=1, locale='en', min_date=date,
                                              max_date=date+datetime.timedelta(days=200)).build()
    bot.send_message(message.chat.id, f"Select a date {LSTEP[step]}", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def cal(callback_query: types.CallbackQuery) -> None:
    """
    Callback func of calendar, print keyboard with date and await answer,
    Put answer to data_storage
    and moves next
    :param callback_query: Callback Query

    """
    date = datetime.date.today()
    result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='en', min_date=date,
                                                 max_date=date+datetime.timedelta(
                                                     days=200)).process(callback_query.data)
    if not result and key:
        bot.edit_message_text(f"Select a date {LSTEP[step]}",
                              callback_query.message.chat.id,
                              callback_query.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You piked {result}",
                              callback_query.message.chat.id,
                              callback_query.message.message_id)
        with bot.retrieve_data(callback_query.message.chat.id, callback_query.message.chat.id) as data:
            data['pick_day_in'] = result
        bot.set_state(callback_query.message.from_user.id, UserSearchState.pick_day_out)
        date_out(callback_query)


def date_out(callback_query: types.CallbackQuery) -> None:
    """
    Function call day to check out
    :param callback_query: Query
    """
    with bot.retrieve_data(callback_query.message.chat.id, callback_query.message.chat.id) as data:
        date_today = data['pick_day_in'] + datetime.timedelta(days=1)
        text = "Select a date of check out"
        bot.send_message(callback_query.message.chat.id, text)
        calendar, step = DetailedTelegramCalendar(calendar_id=2, locale='en', min_date=date_today,
                                                  max_date=date_today+datetime.timedelta(days=200)).build()
        bot.send_message(callback_query.message.chat.id, f"Select a date {LSTEP[step]}", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def cal(callback_query: types.CallbackQuery):
    """
    Callback func of calendar, print keyboard with date and await answer,
    Put answer to data_storage
    and moves next
    :param callback_query: Callback Query
    """
    with bot.retrieve_data(callback_query.message.chat.id, callback_query.message.chat.id) as data:
        date_today = data['pick_day_in'] + datetime.timedelta(days=1)

        result, key, step = DetailedTelegramCalendar(calendar_id=2, locale='en', min_date=date_today,
                                                     max_date=date_today+datetime.timedelta(
                                                         days=200)).process(callback_query.data)
        if not result and key:
            bot.edit_message_text(f"Select a date {LSTEP[step]}",
                                  callback_query.message.chat.id,
                                  callback_query.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"You selected{result}",
                                  callback_query.message.chat.id,
                                  callback_query.message.message_id)
            data['pick_day_out'] = result
            hotels_script.photo_select(callback_query.message)
