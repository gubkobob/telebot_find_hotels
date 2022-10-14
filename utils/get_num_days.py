import datetime

def get_num_days(check_in, check_out):


    year_out = int(check_out[:4])
    day_out = int(check_out[5:7])
    month_out = int(check_out[8:])

    year_in = int(check_in[:4])
    day_in = int(check_in[5:7])
    month_in = int(check_in[8:])

    num = (datetime.datetime(year_out, day_out, month_out) - datetime.datetime(year_in, day_in, month_in)).days

    return num



