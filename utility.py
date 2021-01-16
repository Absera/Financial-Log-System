import datetime


def dateToInt(date):
    try:
        date_format = date.split("-")
        dt = datetime.datetime(int(date_format[0]), int(date_format[1]), int(date_format[2]))
        seq = int(dt.strftime("%Y%m%d"))
        return seq
    except:
        return 00000000


def intToDate(_int):
    try:
        return str(datetime.datetime.strptime(str(_int), '%Y%m%d').date())
    except:
        return datetime.datetime.strptime(00000000, '%Y%m%d').date()



