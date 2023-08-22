from telebot.handler_backends import State, StatesGroup


class FindInfoState(StatesGroup):
    town = State()
    town_area = State()
    check_in = State()
    check_out = State()
    num_hotels = State()
    photo_choise = State()
    num_photo = State()
    put_results = State()
