from utils.get_areas import get_areas
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from utils.get_hotels import get_hotels
from utils.find_lowprice import lowprice

count123 = 0

def city_markup(city):
    cities = get_areas(city)

    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'],
                          callback_data=f'{city["destination_id"]}'))

    return destinations

@bot.message_handler(content_types=['text'])
def start(message):
    bot.send_message(message.chat.id, 'В каком городе ищем?')
    bot.register_next_step_handler(message, city)


def count1(message):
    global count123
    count123 = int(message.text)

def city(message):
    town = message.text
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_markup(town)) # Отправляем кнопки с вариантами

@bot.callback_query_handler(func=lambda call: True)
def callback_place(call):
    place_ID = call.data
    bot.send_message(call.message.chat.id, 'Сколько отелей вывести?')
    bot.register_next_step_handler(call.message, count1)

    hotels = get_hotels(place_ID)
    res_hotels = lowprice(hotels=hotels, count=count123, max_count=10)
    count = 1
    for hotel in res_hotels:
        bot.send_message(call.message.chat.id, str(count))
        for name, item in hotel.items():
            bot.send_message(call.message.chat.id, "{} - {}".format(name, item))
        count += 1


    # print(place_ID)
