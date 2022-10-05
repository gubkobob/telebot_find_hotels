from loader import bot
from states.info_bestdeal import BestdealInfoState
from telebot.types import Message
from telebot.types import InputMediaPhoto
from keyboards.inline.city_choise import city_choise
from keyboards.reply.yes_no_choise import yes_no_choise
from keyboards.reply.ok_choise import ok_choise
from utils.get_hotels_bestdeal import get_hotels_bestdeal
from utils.find_bestdeal import bestdeal
from utils.get_photos import get_photos
from utils.get_areas import get_areas
import re


@bot.message_handler(commands=['bestdeal'])
def survey_bestdeal(message: Message) -> None:
    bot.set_state(message.from_user.id, BestdealInfoState.town, message.chat.id)
    bot.send_message(message.from_user.id, "Введите город для поиска отелей")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["request"] = message.text



@bot.message_handler(state=BestdealInfoState.town)
def get_town(message: Message) -> None:
    if message.text.isalpha():
        if get_areas(message.text):

            bot.send_message(message.from_user.id, "Уточните пожалуйста:", reply_markup=city_choise(message.text))
            bot.set_state(message.from_user.id, BestdealInfoState.town_area, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["town"] = message.text
        else:
            bot.send_message(message.from_user.id, "Такого города в базе нет")

    else:
        bot.send_message(message.from_user.id, "Название города может содержать только буквы")

@bot.message_handler(state=BestdealInfoState.town_area)
def key1(call):
    if bot.get_state(call.from_user.id) == BestdealInfoState.town_area:
        return True
    else:
        return False


@bot.callback_query_handler(func=lambda call: key1(call))
def callback_place1(call):
    if call.data:
        bot.send_message(call.message.chat.id, "Введите минимальную цену номера в отеле")
        bot.set_state(call.from_user.id, BestdealInfoState.min_price)

        with bot.retrieve_data(call.from_user.id) as data:
            data["areaID"] = call.data

        bot.register_next_step_handler(call.message, get_min_price)
    # bot.answer_callback_query(call.id)


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


@bot.message_handler(state=BestdealInfoState.photo_choise)
def callback_if_need_photo(message: Message) -> None:

    with bot.retrieve_data(message.from_user.id) as data:
        data["if_need_photo"] = message.text
        text = "Вам нужно вывести {num_hotels} отеля c ценами {min_price} - {max_price}" \
               " и расстоянием до центра города {min_dist} - {max_dist}?".\
            format(num_hotels=data["num_hotels"],
                   min_price=data["min_price"],
                   max_price=data["max_price"],
                   min_dist=data["min_dist"],
                   max_dist=data["max_dist"]
                   )
    if message.text.lower() == "да":
        bot.send_message(message.from_user.id, "Сколько фото вывести")
        bot.set_state(message.from_user.id, BestdealInfoState.num_photo)
    elif message.text.lower() == "нет":
        bot.set_state(message.from_user.id, BestdealInfoState.put_results)
        bot.send_message(message.from_user.id, text, reply_markup=ok_choise())
    else:
        bot.send_message(message.from_user.id, "Надо нажать на кнопку или написать да/нет")



@bot.message_handler(state=BestdealInfoState.num_photo)
def get_num_photo(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["num_photo"] = int(message.text)
            text1 = "Вам нужно вывести {num_hotels} отеля с {num_photo} фото c ценами {min_price} - {max_price}" \
                   " и расстоянием до центра города {min_dist} - {max_dist}?". \
                format(num_hotels=data["num_hotels"],
                       num_photo=data["num_photo"],
                       min_price=data["min_price"],
                       max_price=data["max_price"],
                       min_dist=data["min_dist"],
                       max_dist=data["max_dist"]
                       )
        bot.set_state(message.from_user.id, BestdealInfoState.put_results, message.chat.id)
        bot.send_message(message.from_user.id, text1, reply_markup=ok_choise())

    else:
        bot.send_message(message.from_user.id, "Количество фото должно быть цифрой")


@bot.message_handler(state=BestdealInfoState.put_results)
def output_res(message: Message) -> None:
    if message.text.lower() == "да":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

            hotels = get_hotels_bestdeal(town_ID=data["areaID"], min_price=data["min_price"], max_price=data["max_price"])

            if data["request"] == "/bestdeal":
               res_hotels = bestdeal(hotels=hotels, count=data["num_hotels"],
                                     min_dist=data["min_dist"], max_dist=data["max_dist"])

            bot.send_message(message.chat.id, "Результаты поиска:\n")
            for hotel in res_hotels:
                text = "Название отеля: {name}\n Адрес: {adress}\n Расстояние до центра: {distance}\n Цена: {price}\n".format(
                    name=hotel["name"],
                    adress=hotel["address"],
                    distance=hotel["distance"],
                    price=hotel["price"],
                )
                # bot.send_message(message.chat.id, text)

                if data["if_need_photo"] == "Да":
                    photos = get_photos(hotel["id"], data["num_photo"])
                    if photos:
                        media_group = []
                        num = 0
                        for photo in photos:

                            media_group.append(InputMediaPhoto(photo, caption=text if num == 0 else ''))
                            num += 1
                        bot.send_media_group(message.chat.id, media=media_group)

                    else:
                        text = "\n".join(text, "У отеля нет фото")
                        bot.send_message(message.chat.id, text)
                else:
                    bot.send_message(message.chat.id, text)

    else:
        bot.send_message(message.chat.id, "Для продолжения нужно нажать на кнопку'да' или написать да")




