import datetime
import re

def check_data_in(data_str):
    pattern = r"\d{4}-\d{2}-\d{2}"
    correctDate = False
    if re.match(pattern, data_str) and len(data_str) == 10:
        year = int(data_str[:4])
        day = int(data_str[5:7])
        month = int(data_str[8:])
        try:
            newDate = datetime.datetime(year, day, month)
        except ValueError:
            correctDate = False
        else:
            if datetime.datetime(year, day, month) < datetime.datetime.now():
                correctDate = False
            else:
                correctDate = True

    return correctDate