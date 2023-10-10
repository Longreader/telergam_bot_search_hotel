from telebot import types
from config_data import config


def isPhotoNeeded() -> types.ReplyKeyboardMarkup:
    """
    Function asks User if photo need in your case
    return None
    :return: None
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Yes')
    btn2 = types.KeyboardButton('No')
    markup.add(btn1, btn2)
    return markup


def numerate() -> types.ReplyKeyboardMarkup:
    """
    Function asks User number
    return None
    :return: None
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for _ in range(1, config.MAX_PHOTOS+1):
        markup.add(types.KeyboardButton(str(_)))
    return markup
