from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.get_areas import get_areas


def city_choise(city):
    cities = get_areas(city)
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(
            InlineKeyboardButton(
                text=city["city_name"], callback_data=f'{city["destination_id"]}'
            )
        )

    return destinations
