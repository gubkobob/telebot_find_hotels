import datetime
import re

def check_data_out(data_str, data_in):
    pattern = r"\d{4}-\d{2}-\d{2}"
    correctDate = False
    year_out = int(data_in[:4])
    day_out = int(data_in[5:7])
    month_out = int(data_in[8:])

    if re.match(pattern, data_str) and len(data_str) == 10:
        year = int(data_str[:4])
        day = int(data_str[5:7])
        month = int(data_str[8:])
        try:
            newDate = datetime.datetime(year, day, month)
        except ValueError:
            correctDate = False
        else:
            if datetime.datetime(year, day, month) < datetime.datetime(year_out,day_out,month_out):
                correctDate = False
            else:
                correctDate = True

    return correctDate