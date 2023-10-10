from telebot.handler_backends import State, StatesGroup


class UserSearchState(StatesGroup):
    """
    Consist user's hotel request states
    """
    id = State()
    command = State()
    location = State()
    pick_day_in = State()
    pick_day_out = State()
    hotel_photo = State()
    photo_nums = State()
    hotels_nums = State()
