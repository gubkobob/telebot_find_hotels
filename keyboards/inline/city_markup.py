from utils.get_areas import get_areas
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot

def city_markup():
    cities = get_areas()

    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'],
                          callback_data=f'{city["destination_id"]}'))
    return destinations

@bot.message_handler(content_types=['text'])
def start(message):
    bot.send_message(message.chat.id, 'В каком городе ищем?')
    bot.register_next_step_handler(message, city)


def city(message):
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_markup()) # Отправляем кнопки с вариантами