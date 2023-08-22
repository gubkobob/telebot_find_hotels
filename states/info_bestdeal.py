from telebot.handler_backends import State, StatesGroup


class BestdealInfoState(StatesGroup):
    town = State()
    town_area = State()
    check_in = State()
    check_out = State()
    min_price = State()
    max_price = State()
    min_dist = State()
    max_dist = State()
    num_hotels = State()
    photo_choise = State()
    num_photo = State()
    put_results = State()
