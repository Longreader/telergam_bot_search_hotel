from telebot import types
from loader import bot
import typing

from logs.log import log_dec

from keyboards.inline.cities_list import city_markup
from keyboards.inline.calendar import set_date_in

from keyboards.reply.selection import isPhotoNeeded
from keyboards.reply.selection import numerate

from states.SearchHotel import UserSearchState

from utils.requests_to_api import hotels_search, photos_search

from database import request_to_db


@bot.message_handler(commands=['lowprice', 'bestprice', 'highprice'])
@log_dec
def select_command(msg: types.Message):
    """
    Start function of /lowprice/bestprice/highprice script
    Storage data : Name of command
    Ask user to write down "city to search"
    :param msg: type Message
    :return: None
    """
    bot.delete_state(msg.chat.id, msg.chat.id)
    bot.set_state(msg.from_user.id, UserSearchState.id)
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        data['id'] = msg.chat.id
    bot.set_state(msg.from_user.id, UserSearchState.command)
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        data['command'] = msg.text

    bot.send_message(msg.from_user.id, 'Please, write a city',
                     reply_markup=types.ReplyKeyboardRemove())

    bot.set_state(msg.from_user.id, UserSearchState.id)


@bot.message_handler(state=UserSearchState.id)
def import_city(msg: types.Message) -> None:
    """
    Function city entering
    Storage data : User ID
    :param msg: Message
    :return: None
    """
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        data['id'] = msg.from_user.id
    bot.set_state(msg.from_user.id, UserSearchState.location)
    tmp_msg = bot.send_message(msg.chat.id, 'Hold on...Operation is running')
    bot.send_message(msg.chat.id, 'Enter city',
                     reply_markup=city_markup(msg.text))
    bot.delete_message(tmp_msg.chat.id, tmp_msg.id)


@bot.callback_query_handler(func=lambda query: query.data.isdigit())
def city_handler(callback_query: types.CallbackQuery) -> None:
    """
    Current city handler
    Storage data : Location ID
    :param callback_query: Callback query
    :return:
    """

    with bot.retrieve_data(callback_query.message.chat.id, callback_query.message.chat.id) as data:
        data['location'] = callback_query.data

    bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.id,)
    bot.set_state(callback_query.message.from_user.id, UserSearchState.pick_day_in)
    set_date_in(callback_query.message)
    bot.set_state(callback_query.message.from_user.id, UserSearchState.hotel_photo)


@bot.message_handler(state=UserSearchState.hotel_photo)
def photo_select(msg: types.Message) -> None:
    """
    Select attaching photos of hotels
    Gives a ReplyKeyboard
    :param msg: User Message
    :return:
    """
    m = bot.send_message(msg.chat.id, 'Attach a photo to each hotel?',
                         reply_markup=isPhotoNeeded())
    bot.register_next_step_handler(m, photo)


def photo(msg: types.Message) -> None:
    """
    Select function
    :param msg: User Message
    :return: None
    """
    if msg.text == 'Yes':
        with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
            data['hotel_photo'] = 1
        bot.set_state(msg.from_user.id, UserSearchState.photo_nums)
        photo_num(msg)
    elif msg.text == 'No':
        with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
            data['hotel_photo'] = 0
        bot.set_state(msg.from_user.id, UserSearchState.photo_nums)
        with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
            data['photo_nums'] = 0
        bot.set_state(msg.from_user.id, UserSearchState.hotels_nums)
        hotels_num(msg)
    else:
        photo_select(msg)


@bot.message_handler(state=UserSearchState.hotels_nums)
def photo_num(msg: types.Message) -> None:
    """
    Select num of each hotel photo (limit is 5)
    :param msg: User Message
    :return: None
    """
    m = bot.send_message(msg.chat.id, 'Select number of photo to each hotel',
                         reply_markup=numerate())
    bot.register_next_step_handler(m, hotels_num)


@bot.message_handler(state=UserSearchState.hotels_nums)
def hotels_num(msg: types.Message) -> None:
    """
    Select num of hotels to show
    :param msg:
    :return:
    """
    if msg.text.isdigit():
        with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
            data['photo_nums'] = msg.text

    m = bot.send_message(msg.chat.id, 'Select number of hotels to show',
                         reply_markup=numerate())
    bot.register_next_step_handler(m, hotel_register)


def hotel_register(msg: types.Message):
    if msg.text.isdigit():
        with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
            data['hotels_nums'] = msg.text
    tmp_msg = bot.send_message(msg.chat.id, 'Hold on...Operation is running',
                               reply_markup=types.ReplyKeyboardRemove())
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        try:
            hotels = hotels_search(data['location'], data['pick_day_in'], data['pick_day_out'],
                                   int(data['hotels_nums']), str(data['command']))
        except Exception:
            bot.send_message('Something went wrong. Check your date.')
            bot.delete_state()
        if hotels == 0:
            bot.send_message(tmp_msg.chat.id, 'Something went wrong')
            select_command(tmp_msg)
    sent_out(hotels, tmp_msg)


def sent_out(hotels: typing.List, old_msg: types.Message):
    msg = bot.send_message(old_msg.chat.id, 'One more second', reply_markup=types.ReplyKeyboardRemove())
    bot.delete_message(old_msg.chat.id, old_msg.id)
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        if data['photo_nums'] == 0:
            for hotel in hotels:
                bot.send_message(msg.chat.id, f'Hotel: {hotel["name"]}\n'
                                              f'Price: per night: '
                                              f'{hotel["price"]["options"][0]["formattedDisplayPrice"]}\n'
                                              f'Distance: '
                                              f'{hotel["destinationInfo"]["distanceFromDestination"]["value"]} miles\n')
                bot.send_location(msg.chat.id,
                                  float(hotel["mapMarker"]["latLong"]["latitude"]),
                                  float(hotel["mapMarker"]["latLong"]["longitude"]))
        else:
            for hotel in hotels:
                try:
                    photos = photos_search(str(hotel["id"]))
                except Exception:
                    bot.send_message(msg.chat.id, 'Something went wrong. Can not upload photo')
                if photos == 0:
                    bot.send_message(msg.chat.id, 'Something went wrong')
                media = list()
                max_photo = int(data["photo_nums"])
                current_num = 0
                for photo in photos:
                    if current_num == 0:
                        media.append(types.InputMediaPhoto(photo["image"]["url"], caption=(
                            f'Hotel: {hotel["name"]}\n'
                            f'Price: per night: {hotel["price"]["options"][0]["formattedDisplayPrice"]}\n'
                            f'Distance: {hotel["destinationInfo"]["distanceFromDestination"]["value"]} miles\n')))
                    else:
                        media.append(types.InputMediaPhoto(photo["image"]["url"]))
                    current_num += 1
                    if max_photo == current_num:
                        break
                bot.send_media_group(msg.chat.id, media)
                bot.send_location(msg.chat.id,
                                  float(hotel["mapMarker"]["latLong"]["latitude"]),
                                  float(hotel["mapMarker"]["latLong"]["longitude"]))

        request_to_db.set_sql(data['id'], data['location'], data['command'], data['hotel_photo'],
                              data['photo_nums'], data['hotels_nums'],
                              data['pick_day_in'], data['pick_day_out'])
    bot.delete_state(msg.chat.id, msg.chat.id)
