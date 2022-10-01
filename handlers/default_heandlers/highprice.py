from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['highprice'])
def bot_highprice(message: Message):
    bot.send_message(message.chat.id, "запуск highprice")



    # bot.reply_to(message, f"бла-бла, {message.from_user.full_name}!")

