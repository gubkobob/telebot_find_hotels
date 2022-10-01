from telebot.types import Message
from loader import bot
from utils.get_hotels import get_hotels
from utils.get_town_ID import get_town_ID
from utils.find_lowprice import lowprice
from keyboards.inline.city_markup import city_markup, start, city


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message):
    start()





    # result = lowprice(get_hotels(get_town_ID("new york")), count=4, max_count=100)
    # bot.reply_to(message, f"Список отелей по возрастанию цены:, {result}")

# print(get_town_ID("new york"))
# print(get_hotels(get_town_ID("new york")))

# print(result)