import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("lowprice", "Вывести список отелей по возрастанию цены"),
    ("highprice", "Вывести список отелей по снижению цены"),
    (
        "bestdeal",
        "Вывести список отелей по лучшему соотношению цена/расстояние до центра города",
    ),
    ("history", "История поисков"),
)
