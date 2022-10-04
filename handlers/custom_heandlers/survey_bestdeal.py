from loader import bot
from states.info_bestdeal import BestdealInfoState
from telebot.types import Message
from keyboards.inline.city_choise import city_choise
from keyboards.reply.yes_no_choise import yes_no_choise
from utils.get_hotels import get_hotels
# from utils.find_lowprice import lowprice
# from utils.find_highprice import highprice
from utils.get_photos import get_photos
from utils.get_areas import get_areas
import re


@bot.message_handler(commands=['bestprice'])
def survey_bestdeal(message: Message) -> None:
    bot.set_state(message.from_user.id, BestdealInfoState.town, message.chat.id)
    bot.send_message(message.from_user.id, "Введите город для поиска отелей")

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     data["request"] = message.text



@bot.message_handler(state=BestdealInfoState.town)
def get_town(message: Message) -> None:
    if message.text.isalpha():
        if get_areas(message.text):

            bot.send_message(message.from_user.id, "Уточните пожалуйста:", reply_markup=city_choise(message.text))

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["town"] = message.text
        else:
            bot.send_message(message.from_user.id, "Такого города в базе нет")

    else:
        bot.send_message(message.from_user.id, "Название города может содержать только буквы")


@bot.callback_query_handler(func=lambda call: True)
def callback_place(call):
    if call.data:
        bot.send_message(call.message.chat.id, "Введите минимальную цену номера в отеле")
        bot.set_state(call.from_user.id, BestdealInfoState.min_price)

        with bot.retrieve_data(call.from_user.id) as data:
            data["areaID"] = call.data

        bot.register_next_step_handler(call.message, get_min_price)


@bot.message_handler(state=BestdealInfoState.min_price)
def get_min_price(message: Message) -> None:
    if message.text.isdigit():
        bot.set_state(message.from_user.id, BestdealInfoState.max_price, message.chat.id)
        bot.send_message(message.from_user.id, "Введите максимальную цену номера в отеле")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["min_price"] = int(message.text)

    else:
        bot.send_message(message.from_user.id, "Минимальная цена это натуральное число")


@bot.message_handler(state=BestdealInfoState.max_price)
def get_max_price(message: Message) -> None:
    if message.text.isdigit():
        bot.set_state(message.from_user.id, BestdealInfoState.min_dist, message.chat.id)
        bot.send_message(message.from_user.id, "Введите минимальное расстояние до центра города в км")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["max_price"] = int(message.text)

    else:
        bot.send_message(message.from_user.id, "Максимальная цена это натуральное число")


@bot.message_handler(state=BestdealInfoState.min_dist)
def get_min_dist(message: Message) -> None:
    pattern = r"\d+\.{0,1}\d*"
    if re.match(pattern, message.text):

        bot.set_state(message.from_user.id, BestdealInfoState.max_dist, message.chat.id)
        bot.send_message(message.from_user.id, "Введите максимальное расстояние до центра города в км")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["min_dist"] = float(message.text)

    else:
        bot.send_message(message.from_user.id, "расстояние надо вводить в формате n или n.n")


@bot.message_handler(state=BestdealInfoState.max_dist)
def get_max_dist(message: Message) -> None:
    pattern = r"\d+\.{0,1}\d*"
    if re.match(pattern, message.text):

        bot.set_state(message.from_user.id, BestdealInfoState.num_hotels, message.chat.id)
        bot.send_message(message.from_user.id, "Сколько отелей вывести в результате")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["max_dist"] = float(message.text)

    else:
        bot.send_message(message.from_user.id, "расстояние надо вводить в формате n или n.n")




@bot.message_handler(state=BestdealInfoState.num_hotels)
def get_num_hotels(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Нужны ли Вам фото отелей", reply_markup=yes_no_choise())
        bot.set_state(message.from_user.id, BestdealInfoState.photo_choise, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["num_hotels"] = int(message.text)
    else:
        bot.send_message(message.from_user.id, "Количество отелей должно быть цифрой")



#################




@bot.message_handler(state=BestdealInfoState.photo_choise)
def callback_if_need_photo(message: Message) -> None:

    with bot.retrieve_data(message.from_user.id) as data:
        data["if_need_photo"] = message.text

    if message.text == "Да":
        bot.send_message(message.from_user.id, "Сколько фото вывести")
        bot.set_state(message.from_user.id, FindInfoState.num_photo)
    elif message.text == "Нет":
        bot.set_state(message.from_user.id, FindInfoState.put_results)


@bot.message_handler(state=FindInfoState.num_photo)
def get_num_photo(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["num_photo"] = int(message.text)
        bot.set_state(message.from_user.id, FindInfoState.put_results, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Количество фото должно быть цифрой")


@bot.message_handler(state=FindInfoState.put_results)
def output_res(message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        print(data)

        hotels = get_hotels(data["areaID"])

        if data["request"] == "/lowprice":
            res_hotels = lowprice(hotels=hotels, count=data["num_hotels"], max_count=10)
        elif data["request"] == "/highprice":
            res_hotels = highprice(hotels=hotels, count=data["num_hotels"], max_count=10)

        bot.send_message(message.chat.id, "Результаты поиска:\n")
        for hotel in res_hotels:
            text = "Название отеля: {name}\n Адрес: {adress}\n Расстояние до центра: {distance}\n Цена: {price}\n".format(
                name=hotel["name"],
                adress=hotel["address"],
                distance=hotel["distance"],
                price=hotel["price"],
            )
            bot.send_message(message.chat.id, text)

            if data["if_need_photo"] == "Да":
                photos = get_photos(hotel["id"], data["num_photo"])
                if photos:
                    bot.send_message(message.chat.id, "Фото:")
                    for photo in photos:
                        with open(str(photo).format("s"), "rb") as photo_data:
                            bot.send_photo(message.chat.id, photo_data)
                else:
                    bot.send_message(message.chat.id, "Нет фото для этого отеля")



