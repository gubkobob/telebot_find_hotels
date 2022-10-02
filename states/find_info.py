from telebot.handler_backends import State, StatesGroup

class FindInfoState(StatesGroup):
    town = State()
    town_area = State()
    num_hotels = State()
    photo_choise = State()
    num_photo = State()