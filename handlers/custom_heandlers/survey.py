from loader import bot
from states.find_info import FindInfoState
from telebot.types import Message
from telebot.types import InputMediaPhoto
from keyboards.inline.city_choise import city_choise
from keyboards.reply.yes_no_choise import yes_no_choise
from keyboards.reply.ok_choise import ok_choise
from utils.get_hotels import get_hotels
from utils.find_lowprice import lowprice
from utils.find_highprice import highprice
from utils.get_photos import get_photos
from utils.get_areas import get_areas
from database.db_hotels import *
from datetime import datetime
from utils.check_data_in import check_data_in
from utils.check_data_out import check_data_out
from utils.get_num_days import get_num_days


@bot.message_handler(state="*", commands=["lowprice", "highprice"])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, FindInfoState.town, message.chat.id)
    bot.send_message(message.from_user.id, "Введите город для поиска отелей")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["request"] = message.text


@bot.message_handler(state=FindInfoState.town)
def get_town(message: Message) -> None:
    if message.text.isalpha():
        if get_areas(message.text):
            bot.send_message(
                message.from_user.id,
                "Уточните пожалуйста:",
                reply_markup=city_choise(message.text),
            )
            bot.set_state(
                message.from_user.id, FindInfoState.town_area, message.chat.id
            )

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["town"] = message.text
        else:
            bot.send_message(message.from_user.id, "Такого города в базе нет")

    else:
        bot.send_message(
            message.from_user.id, "Название города может содержать только буквы"
        )


@bot.message_handler(state=FindInfoState.town_area)
def key(call):
    if bot.get_state(call.from_user.id) == FindInfoState.town_area:
        return True
    else:
        return False


@bot.callback_query_handler(func=lambda call: key(call))
def callback_place(call):
    if call.data:
        bot.send_message(
            call.message.chat.id,
            "Введите дату заезда в формате YYYY-MM-DD не ранее завтра",
        )
        bot.set_state(call.from_user.id, FindInfoState.check_in)

        with bot.retrieve_data(call.from_user.id) as data:
            data["areaID"] = call.data

        bot.register_next_step_handler(call.message, get_check_in)


@bot.message_handler(content_types=["text"], state=FindInfoState.town_area)
def error(message: Message) -> None:
    bot.send_message(message.from_user.id, "Надо выбрать область из списка")


@bot.message_handler(state=FindInfoState.check_in)
def get_check_in(message: Message) -> None:
    if check_data_in(message.text):
        bot.send_message(
            message.from_user.id,
            "Введите дату выезда в формате YYYY-MM-DD не ранее даты заезда",
        )
        bot.set_state(message.from_user.id, FindInfoState.check_out, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["check_in"] = message.text
    else:
        bot.send_message(
            message.from_user.id, "Дата в формате YYYY-MM-DD не ранее завтра!!!"
        )


@bot.message_handler(state=FindInfoState.check_out)
def get_check_out(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if check_data_out(message.text, data["check_in"]):
            bot.send_message(
                message.from_user.id, "Сколько отелей вывести в результате"
            )
            bot.set_state(
                message.from_user.id, FindInfoState.num_hotels, message.chat.id
            )

            data["check_out"] = message.text
        else:
            bot.send_message(
                message.from_user.id,
                "Дата в формате YYYY-MM-DD не ранее даты заезда!!!",
            )


@bot.message_handler(state=FindInfoState.num_hotels)
def get_num_hotels(message: Message) -> None:
    if message.text.isdigit() and int(message.text) > 0:
        bot.send_message(
            message.from_user.id,
            "Нужны ли Вам фото отелей",
            reply_markup=yes_no_choise(),
        )
        bot.set_state(message.from_user.id, FindInfoState.photo_choise, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["num_hotels"] = int(message.text)
    else:
        bot.send_message(
            message.from_user.id, "Количество отелей должно быть цифрой > 0"
        )


@bot.message_handler(state=FindInfoState.photo_choise)
def callback_if_need_photo(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        data["if_need_photo"] = message.text
        text = "Вам нужно вывести {} отеля?".format(data["num_hotels"])
    if message.text.lower() == "да":
        bot.send_message(message.from_user.id, "Сколько фото вывести")
        bot.set_state(message.from_user.id, FindInfoState.num_photo)
    elif message.text.lower() == "нет":
        bot.set_state(message.from_user.id, FindInfoState.put_results)
        bot.send_message(message.from_user.id, text, reply_markup=ok_choise())
    else:
        bot.send_message(
            message.from_user.id, "Надо нажать на кнопку или написать да/нет"
        )


@bot.message_handler(state=FindInfoState.num_photo)
def get_num_photo(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["num_photo"] = int(message.text)
            text1 = "Вам нужно вывести {} отеля с {} фото?".format(
                data["num_hotels"], data["num_photo"]
            )
        bot.set_state(message.from_user.id, FindInfoState.put_results, message.chat.id)
        bot.send_message(message.from_user.id, text1, reply_markup=ok_choise())

    else:
        bot.send_message(message.from_user.id, "Количество фото должно быть цифрой")


@bot.message_handler(state=FindInfoState.put_results)
def output_res(message: Message) -> None:
    if message.text.lower() == "да":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            # print(data)

            hotels = get_hotels(
                town_ID=data["areaID"],
                checkIn=data["check_in"],
                checkOut=data["check_out"],
            )

            if data["request"] == "/lowprice":
                res_hotels = lowprice(
                    hotels=hotels, count=data["num_hotels"], max_count=10
                )
            elif data["request"] == "/highprice":
                res_hotels = highprice(
                    hotels=hotels, count=data["num_hotels"], max_count=10
                )

            if not Person.select().where(Person.telegram_id == message.from_user.id):
                my_person = Person.create(
                    telegram_id=message.from_user.id, name=message.from_user.full_name
                )
            else:
                my_person = Person.get(Person.telegram_id == message.from_user.id)

            my_datetime = datetime.now()
            db_datetime = DateTime.create(
                name_id=my_person, when=my_datetime, command=data["request"]
            )

            bot.send_message(message.chat.id, "Результаты поиска:\n")

            if len(res_hotels) > 0:
                for hotel in res_hotels:
                    text = "Название отеля: {name}\n Адрес: {adress}\n Расстояние до центра: {distance}\n Цена: {price}\n".format(
                        name=hotel["name"],
                        adress=hotel["address"],
                        distance=hotel["distance"],
                        price=hotel["price"]
                        * get_num_days(
                            check_in=data["check_in"], check_out=data["check_out"]
                        ),
                    )

                    Hotels.create(name_hotel=hotel["name"], name_hotel_when=db_datetime)

                    if data["if_need_photo"] == "Да":
                        photos = get_photos(hotel["id"], data["num_photo"])
                        if photos:
                            media_group = []

                            num = 0
                            for photo in photos:
                                media_group.append(
                                    InputMediaPhoto(
                                        photo, caption=text if num == 0 else ""
                                    )
                                )
                                num += 1
                            bot.send_media_group(message.chat.id, media=media_group)

                        else:
                            text = "\n".join(text, "У отеля нет фото")
                            bot.send_message(message.chat.id, text)

                    else:
                        bot.send_message(message.chat.id, text)
            else:
                bot.send_message(message.chat.id, "нет результатов")

        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            "Для продолжения нужно нажать на кнопку'да' или написать да",
        )
