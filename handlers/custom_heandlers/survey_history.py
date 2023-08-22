from loader import bot
from telebot.types import Message
from database.db_hotels import *


@bot.message_handler(state="*", commands=["history"])
def survey(message: Message) -> None:
    text_full = []
    for my_time in (
        DateTime.select().join(Person).where(Person.telegram_id == message.from_user.id)
    ):
        who = my_time.name_id.name
        command = my_time.command
        time1 = my_time.when
        hotels = ""
        for hotel in Hotels.select().where(Hotels.name_hotel_when == my_time):
            hotels += str(hotel.name_hotel)
            hotels += ", "

        text = "Искал пользователь {}, комманда - {}, время - {}, найденные отели: {}.".format(
            who, command, time1, hotels
        )
        text_full.append(text)
    bot.send_message(message.from_user.id, "\n".join(text_full))
