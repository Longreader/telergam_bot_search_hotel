from config_data import config
import datetime
import json
from loguru import logger
import requests
import typing
from utils.utils_funcs import separate


def location_search(city: str) -> typing.List[typing.Any]:
    """
    Sent request to 'v2/search' Hotels API
    :param city: Message of User
    :return: Location of cities
    """
    cities = list()
    querystring = {
        "q": city.capitalize(),
        "locate": "en_US",
    }
    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.RAPID_API_HOST
    }
    try:
        response = requests.request("GET", config.CITY_URL, headers=headers, params=querystring, timeout=30)
        if response.status_code == requests.codes.ok:
            json_response = json.loads(response.text)
            cities = json_response["sr"]
            return cities
        else:
            logger.exception('Connection ERROR')
    except Exception as ex:
        logger.exception(f'Something went wrong {ex}')


def hotels_search(region_id: int | str,
                  check_in: datetime.time | str,
                  check_out: datetime.time | str,
                  hotel_num: int,
                  command: str) -> typing.Iterable:
    """
    Request to API "hotels/list" Hotels API
    :param region_id: ID of current search region
    :param check_in: Date of User check in
    :param check_out: Date of user check out
    :param hotel_num: Nuber of hotel
    :param command: User command
    :return:
    """
    move_in = separate(check_in)
    move_out = separate(check_out)
    logger.debug(f'request_to_api -> hotel_search :: {move_out[::]}')

    filter = ''
    if command == '/lowprice':
        filter = 'PRICE_LOW_TO_HIGH'
    elif command == '/bestprice':
        filter = 'PRICE_RELEVANT'
    elif command == '/highprice':
        filter = 'PRICE_HIGH_TO_LOW'

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": {
            "day": move_in[1],
            "month": move_in[0],
            "year": move_in[2]
        },
        "checkOutDate": {
            "day": move_out[1],
            "month": move_out[0],
            "year": move_out[2]
        },
        "rooms": [
            {
                "adults": 1
                # "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": hotel_num,
        "sort": filter
        # "filters": {"price": {
        #     "max": 150,
        #     "min": 0
        # }}
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.RAPID_API_HOST
    }
    try:
        response = requests.request("POST", config.HOTEL_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == requests.codes.ok:
            json_response = json.loads(response.text)
            hotels = json_response["data"]['propertySearch']['properties']
            return hotels
        else:
            logger.exception('Connection ERROR')
    except Exception as ex:
        logger.exception(f'Something went wrong {ex}')


def photos_search(prop_id: str) -> typing.Iterable:
    """
    API req to get hotels photo
    :param prop_id: ID of hotel
    :return:
    """
    logger.debug(f"id is {prop_id}")
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": prop_id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.RAPID_API_HOST
    }
    try:
        response = requests.request("POST", config.PHOTO_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == requests.codes.ok:
            json_response = json.loads(response.text)
            photos = json_response["data"]["propertyInfo"]["propertyGallery"]["images"]
            return photos
        else:
            logger.exception('Connection ERROR')
    except Exception as ex:
        logger.exception(f'Something went wrong {ex}')
