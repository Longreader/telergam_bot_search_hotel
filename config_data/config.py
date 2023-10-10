import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Env file .env is not exist')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
RAPID_API_HOST = 'hotels4.p.rapidapi.com'
DB_HOST_NAME = 'database/hotels.db'
CITY_URL = 'https://hotels4.p.rapidapi.com/locations/v3/search'
HOTEL_URL = 'https://hotels4.p.rapidapi.com/properties/v2/list'
PHOTO_URL = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
MAX_PHOTOS = 5
MAX_HOTELS = 5
DEFAULT_COMMANDS = (
    ('start', "Get started"),
    ('help', "Information"),
    ('lowprice', 'Lowest hotels price'),
    ('highprice', 'The highest hotels price'),
    ('bestprice', 'The best hotel by price and rating'),
    ('history', 'History')
)