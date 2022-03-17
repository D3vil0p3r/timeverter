import time
import datetime

#NOTE: utcfromtimestamp(0) starts at 1970-01-01 00:00:00; fromtimestamp(0) starts at 1970-01-01 XX:00:00 where XX depends on your local time, so be careful.

def datetime_to_float(d):
    epoch = datetime.datetime.utcfromtimestamp(0) #NOTE: used utcfromtimestamp(0) and not fromtimestamp(0) because this function is used only on utc functions
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds

def float_to_datetime(fl):
    return datetime.datetime.utcfromtimestamp(fl)

def current_local_date():
    now = datetime.datetime.now()
    return now

def current_local_epoch():
    epoch = (current_local_date() - datetime.datetime.fromtimestamp(0)).total_seconds()
    return epoch

def current_utc_date(utc):
    hours, minutes = map(float, utc.split(':'))
    utcnow = float_to_datetime(datetime_to_float(datetime.datetime.utcnow()) + ((3600.00 * hours) + (60.00 * minutes)))
    return utcnow

def current_utc_epoch(utc):
    epoch = (current_utc_date(utc) - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    return epoch

def date_to_epoch(date):
    my_date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    t = datetime.datetime(my_date.year, my_date.month, my_date.day, my_date.hour, my_date.minute, my_date.second)
    epoch = (t - datetime.datetime.fromtimestamp(0)).total_seconds()
    return epoch

def epoch_to_date(epoch):
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
    return date_time