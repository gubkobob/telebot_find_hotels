from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def ok_choise():
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton("Да"))
    return keyboard

