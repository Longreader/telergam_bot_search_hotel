import typing

from telebot import types
from loguru import logger

from utils import requests_to_api


def city_markup(city: str) -> types.InlineKeyboardMarkup:
    """
    Inline method choosing city
    :param city: User message contain CITY name
    :return: Buttons of city variation
    """
    cities = requests_to_api.location_search(city)
    destinations = types.InlineKeyboardMarkup()
    for city in cities:
        property_type = city["type"]
        if property_type == "CITY" or property_type == "NEIGHBORHOOD":
            city_name = city["regionNames"]["fullName"]
            city_id = city["gaiaId"]
            destinations.add(types.InlineKeyboardButton(text=city_name,
                                                        callback_data=city_id))
            logger.debug(f'{city_name} === {city_id}')
    return destinations
