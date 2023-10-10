from telebot import types
from loader import bot
from database import request_to_db
from utils.requests_to_api import hotels_search, photos_search
from logs import log


@log.log_dec
@bot.message_handler(commands=['history'])
def history(msg: types.Message) -> None:
    """
    Send to User history of search
    from database (SQLLite)
    :param msg: Message from User
    :return: None
    """
    reply = request_to_db.get_sql(int(msg.chat.id))
    for line in reply:
        tmp = line
        bot.send_message(msg.chat.id, f'The command: {str(tmp[2])}\n'
                                      f'Number of hotels is {int(tmp[5])}\n'
                                      f'Photo status: {bool(tmp[3])}')
        try:
            hotels = hotels_search(str(tmp[1]), str(tmp[6]), str(tmp[7]), int(tmp[5]), str(tmp[2]))
        except Exception:
            bot.send_message('Something went wrong. Check your date.')
            bot.delete_state()

        if tmp[3] == 0:
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
                max_photo = int(tmp[4])
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
