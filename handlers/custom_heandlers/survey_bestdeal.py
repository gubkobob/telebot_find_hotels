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
from database.db_hotels import *
from datetime import datetime
from utils.check_data_in import check_data_in
from utils.check_data_out import check_data_out
from utils.get_num_days import get_num_days



@bot.message_handler(state="*", commands=['bestdeal'])
def survey_bestdeal(message: Message) -> None:
    bot.set_state(message.from_user.id, BestdealInfoState.town, message.chat.id)
    bot.send_message(message.from_user.id, " Введите город для поиска отелей.")

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
            bot.send_message(call.message.chat.id, "Введите дату заезда в формате YYYY-MM-DD не ранее завтра")
            bot.set_state(call.from_user.id, BestdealInfoState.check_in)

            with bot.retrieve_data(call.from_user.id) as data:
                data["areaID"] = call.data

            bot.register_next_step_handler(call.message, get_check_in)

@bot.message_handler(content_types=["text"], state=BestdealInfoState.town_area)
def error(message: Message) -> None:
    bot.send_message(message.from_user.id, "Надо выбрать область из списка")






@bot.message_handler(state=BestdealInfoState.check_in)
def get_check_in(message: Message) -> None:
    if check_data_in(message.text):
        bot.send_message(message.from_user.id, "Введите дату выезда в формате YYYY-MM-DD не ранее даты заезда")
        bot.set_state(message.from_user.id, BestdealInfoState.check_out, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["check_in"] = message.text
    else:
        bot.send_message(message.from_user.id, "Дата в формате YYYY-MM-DD не ранее завтра!!!")


@bot.message_handler(state=BestdealInfoState.check_out)
def get_check_out(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if check_data_out(message.text, data["check_in"]):
            bot.send_message(message.from_user.id, "Введите минимальную цену номера в отеле")
            bot.set_state(message.from_user.id, BestdealInfoState.min_price, message.chat.id)

            data["check_out"] = message.text
        else:
            bot.send_message(message.from_user.id, "Дата в формате YYYY-MM-DD не ранее даты заезда!!!")




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
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if int(message.text) >= data["min_price"]:
                data["max_price"] = int(message.text)
                bot.set_state(message.from_user.id, BestdealInfoState.min_dist, message.chat.id)
                bot.send_message(message.from_user.id, "Введите минимальное расстояние до центра города в км")
            else:
                bot.send_message(message.from_user.id, "Максимальная цена не может быть меньше минимальной")
    else:
        bot.send_message(message.from_user.id, "Максимальная цена это натуральное число")


@bot.message_handler(state=BestdealInfoState.min_dist)
def get_min_dist(message: Message) -> None:

    try:
        float(message.text)
    except Exception:
        bot.send_message(message.from_user.id, "расстояние - число в формате n или n.n")
    else:
        bot.set_state(message.from_user.id, BestdealInfoState.max_dist, message.chat.id)
        bot.send_message(message.from_user.id, "Введите максимальное расстояние до центра города в км")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["min_dist"] = float(message.text)



@bot.message_handler(state=BestdealInfoState.max_dist)
def get_max_dist(message: Message) -> None:

    try:
        float(message.text)
    except Exception:
        bot.send_message(message.from_user.id, "расстояние - число в формате n или n.n")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if float(message.text) >= data["min_dist"]:
                bot.set_state(message.from_user.id, BestdealInfoState.num_hotels, message.chat.id)
                bot.send_message(message.from_user.id, "Сколько отелей вывести в результате")
                data["max_dist"] = float(message.text)
            else:
                bot.send_message(message.from_user.id, "Максимальное расстояние не может быть меньше минимального")



@bot.message_handler(state=BestdealInfoState.num_hotels)
def get_num_hotels(message: Message) -> None:
    if message.text.isdigit() and int(message.text) > 0:
        bot.send_message(message.from_user.id, "Нужны ли Вам фото отелей", reply_markup=yes_no_choise())
        bot.set_state(message.from_user.id, BestdealInfoState.photo_choise, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["num_hotels"] = int(message.text)
    else:
        bot.send_message(message.from_user.id, "Количество отелей должно быть цифрой > 0")


@bot.message_handler(state=BestdealInfoState.photo_choise)
def callback_if_need_photo(message: Message) -> None:

    with bot.retrieve_data(message.from_user.id) as data:
        data["if_need_photo"] = message.text
        text = "Вам нужно вывести {num_hotels} отеля c ценами {min_price} - {max_price} руб" \
               " и расстоянием до центра города {min_dist} - {max_dist} км?".\
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
            text1 = "Вам нужно вывести {num_hotels} отеля с {num_photo} фото c ценами {min_price} - {max_price} руб" \
                   " и расстоянием до центра города {min_dist} - {max_dist} км?". \
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

            hotels = get_hotels_bestdeal(town_ID=data["areaID"],
                                         min_price=data["min_price"],
                                         max_price=data["max_price"],
                                         checkIn=data["check_in"],
                                         checkOut=data["check_out"])

            if data["request"] == "/bestdeal":
               res_hotels = bestdeal(hotels=hotels, count=data["num_hotels"],
                                     min_dist=data["min_dist"], max_dist=data["max_dist"])

            if not Person.select().where(Person.telegram_id == message.from_user.id):
                my_person = Person.create(telegram_id=message.from_user.id, name=message.from_user.full_name)
            else:
                my_person = Person.get(Person.telegram_id == message.from_user.id)

            my_datetime = datetime.now()
            db_datetime = DateTime.create(name_id=my_person, when=my_datetime, command=data["request"])

            bot.send_message(message.chat.id, "Результаты поиска:\n")

            if len(res_hotels) > 0:

                for hotel in res_hotels:
                    text = "Название отеля: {name}\n Адрес: {adress}\n Расстояние до центра: {distance}\n Цена: {price}\n".format(
                        name=hotel["name"],
                        adress=hotel["address"],
                        distance=hotel["distance"],
                        price=hotel["price"] * get_num_days(check_in=data["check_in"], check_out=data["check_out"]),
                    )
                    Hotels.create(name_hotel=hotel["name"], name_hotel_when=db_datetime)


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
                bot.send_message(message.chat.id, "Нет отелей с такими параметрами")


        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Для продолжения нужно нажать на кнопку'да' или написать да")




