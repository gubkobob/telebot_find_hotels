from loader import bot
from states.find_info import FindInfoState
from telebot.types import Message
from keyboards.inline.city_choise import city_choise
from keyboards.reply.yes_no_choise import yes_no_choise
from utils.get_hotels import get_hotels
from utils.find_lowprice import lowprice
from utils.find_highprice import highprice
from utils.get_photos import get_photos


@bot.message_handler(commands=['lowprice', 'highprice'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, FindInfoState.town, message.chat.id)
    bot.send_message(message.from_user.id, "Введите город для поиска отелей")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["request"] = message.text
    # print(message.text)


@bot.message_handler(state=FindInfoState.town)
def get_town(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Уточните пожалуйста:", reply_markup=city_choise(message.text))
        bot.set_state(message.from_user.id, FindInfoState.town_area, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["town"] = message.text

    else:
        bot.send_message(message.from_user.id, "Название города может содержать только буквы")
    # print(message)

@bot.callback_query_handler(func=lambda call: True)#, state=FindInfoState.town_area)
def callback_place(call):
    bot.send_message(call.message.chat.id, "Сколько отелей вывести в результате")
    bot.set_state(call.from_user.id, FindInfoState.num_hotels)

    with bot.retrieve_data(call.from_user.id) as data:
        data["areaID"] = call.data

    bot.register_next_step_handler(call.message, get_num_hotels)




@bot.message_handler(state=FindInfoState.num_hotels)
def get_num_hotels(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Нужны ли Вам фото отелей", reply_markup=yes_no_choise())
        bot.set_state(message.from_user.id, FindInfoState.photo_choise, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["num_hotels"] = int(message.text)
    else:
        bot.send_message(message.from_user.id, "Количество отелей должно быть цифрой")


@bot.message_handler(state=FindInfoState.photo_choise)
def callback_if_need_photo(message: Message) -> None:

    with bot.retrieve_data(message.from_user.id) as data:
        data["if_need_photo"] = message.text

    if message.text == "Да":
        bot.send_message(message.from_user.id, "Сколько фото вывести")
        bot.set_state(message.from_user.id, FindInfoState.num_photo)
    elif message.text == "Нет":
        bot.set_state(message.from_user.id, FindInfoState.exit)

    # print(data["if_need_photo"])


@bot.message_handler(state=FindInfoState.num_photo)
def get_num_photo(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["num_photo"] = int(message.text)
        bot.set_state(message.from_user.id, FindInfoState.exit, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Количество фото должно быть цифрой")

@bot.message_handler(state=FindInfoState.exit)
def output_res(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

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
                bot.send_message(message.chat.id, "Фото:")
                for photo in get_photos(hotel["id"], data["num_photo"]):
                    bot.send_photo(message.chat.id, str(photo).format("s"))






