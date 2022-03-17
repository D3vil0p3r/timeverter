#!/usr/bin/env python
import time
import datetime
import argparse
import base64, zlib
import requests
import hashlib
from urllib.parse import urlparse # python2: from urlparse import urlparse
import http.client # python2: httplib
from sys import stdout
import re
import random

############################################################
# Help                                                     #
############################################################
def help():
   # Display Help
   print_banner()
   print("TimeVerter helps you to bruteforce several kinds of time-based tokens and to convert several time domains.\n")
   
   print("date format: [%YYYY-%mm-%ddT%HH-%MM-%SS]")
   print("epoch format: [seconds]\n")

   print("List of arguments:\n")
   
   print("-c, --colored               let's give some random colored output")
   print("-d DATA, --data DATA        insert data for POST request (i.e. userid=user token=VERTER)")
   print("-D DATE, --date DATE        convert a date to epoch time format")
   print("-div N, --divide N          divide the timestamp by the specified value (used for change the order of magnitude)")
   print("-e EPOCH, --epoch EPOCH     convert epoch time to date format")
   print("-f, --float N               deal timestamp as floating point number and specify the floating step value when range option is set")
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
   print("-x, --method METHOD         specify the HTTP method [default:GET]")
   print("\n")
   print("Use VERTER string on the parameter to bruteforce. Choose -n, -U or -e option for specifying the Time Base of your attack.")
   print("\n")
   print("Usage examples:")
   print("python timeverter.py -d 2022-03-26T01:13:37 -e 1647135274")
   print("python timeverter.py --utc=-3:30")
   print("python timeverter.py -U +0:00 -r 3000 -g md5 -x POST -u http://SERVER_IP:PORT/somefolder/ -d submit=check token=VERTER -fr \"Wrong token\" -mul 1000 -p admin")

class colors:
    '''Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold'''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
        random='\033['+random.choice(['0','33','92','93','94','96'])+'m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'


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

def print_banner():
    #cat banner.txt | gzip | base64
    encoded_data = "H4sIAAAAAAAAA11RW47DIAz85xTzR5Aas7S7bbc5xF4AyRwkh68fQJM1ssEzFhgPoMZuOFmwmFnphZPyVqPBOeS+BGniVU6o4UR9llTl4FdmdY/qlQc1zNr5IEzRkEYTpEhrBMoVbaVGo6FLRCl+Lmg0mskoX6Nl4IrqxLbNJ3LfXy9j9h2/wCr25/hNoOAF+G/b5s/UiucB/pZ3e1+1ER4d/sElzt9GkvaZ78zyHYrzy8uiMCuc0kQ5pcnPScRVBzGPAewTPE7z0FXYsZs8XUs2DXhmxpuopqfS5iNTfsipm6s4Mr1fq0xSxVFPmfDhDQApq7V0AgAA"
    banner = zlib.decompress(base64.b64decode(encoded_data), 16 + zlib.MAX_WBITS).decode('utf-8')
    print(banner)

def print_settings(args):
    print_banner()
    print("________________________________________________")
    print("")
    if args.method:
        print("[*] Method           : %s" % args.method)
    if args.url:
        print("[*] URL              : %s" % args.url)
    if args.data:
        print("[*] Parameters       : %s" % args.data)
    if args.now:
        tb = "Current Local Time"
    elif args.utc:
        tb = ''.join(["Current UTC",args.utc," Time"])
    elif args.epoch:
        tb = ''.join(["Epoch Time: ",str(args.epoch),"; Date Time: ",epoch_to_date(args.epoch)])
    if args.now or args.utc or args.epoch:
        print("[*] Time Base        : %s" % tb)
    if args.range:
        print("[*] Time Range       : %s" % args.range)
    if args.multiply:
        print("[*] Time Multiply Factor  : %d" % args.multiply)
    if args.divide:
        print("[*] Time Divide Factor    : %d" % args.divide)
    if args.algorithm:
        print("[*] Algorithm        : %s" % args.algorithm)
    if args.prefix:
        print("[*] Prefix           : %s" % args.prefix)
    if args.suffix:
        print("[*] Suffix           : %s" % args.suffix)
    if args.matchregex:
        print("[*] Matcher          : regexp -> %s" % args.matchregex)
    if args.filterregex:
        print("[*] Filter           : regexp -> %s" % args.filterregex)
    if args.float:
        print("[*] Float Step value : %f" % args.float)
    print("________________________________________________")
    print("")

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

def define_time(now_time,utc_time,epoch_time,mul,div):
    if now_time:
        ts = current_local_epoch()
    elif utc_time:
        ts = current_utc_epoch(utc_time)
    elif epoch_time:
        ts = epoch_time
    else:
        print("Error! Time parameter not defined")
        exit()

    if mul:
        ts *= mul #(i.e. *1000 = milliseconds)
    elif div:
        ts /= div

    return ts

def compute_token(alg,ts,prefix,suffix):
    if not alg:
        print ("Error! Specify an algorithm.")
        exit()
    
    if alg == "md5":
        token = hashlib.md5((prefix + str(ts) + suffix).encode()).hexdigest()
    elif alg == "sha1":
        token = hashlib.sha1((prefix + str(ts) + suffix).encode()).hexdigest()
    elif alg == "sha224":
        token = hashlib.sha224((prefix + str(ts) + suffix).encode()).hexdigest()
    elif alg == "sha256":
        token = hashlib.sha256((prefix + str(ts) + suffix).encode()).hexdigest()
    elif alg == "sha384":
        token = hashlib.sha384((prefix + str(ts) + suffix).encode()).hexdigest()
    elif alg == "sha512":
        token = hashlib.sha512((prefix + str(ts) + suffix).encode()).hexdigest()
    #### can also add OpenSSL algo...
    return token

def token_request(args):
    print_settings(args)
    
    prefix_str = args.prefix
    suffix_str = args.suffix
    now_time = args.now
    utc_time = args.utc
    date_time = args.date
    epoch_time = args.epoch
    mul = args.multiply
    div = args.divide
    flt = args.float
    alg = args.algorithm
    matchregex = args.matchregex
    filterregex = args.filterregex

    key_token_param_index = "VERTER"
    url = args.url
    if not check_url(url):
        print("Error. Target URL is not responsing.")
        exit()
    
    if not flt:
        rng = args.range
        inc = 1
        ts = int(define_time(now_time,utc_time,epoch_time,mul,div))
    else:
        rng = float(args.range)
        inc = flt
        ts = define_time(now_time,utc_time,epoch_time,mul,div)

    dt = ts - rng
    while dt <= ts + rng:
        hashed_token = compute_token(alg,dt,prefix_str,suffix_str)
        data = args.data
        data[list(data.keys())[list(data.values()).index(key_token_param_index)]] = hashed_token #'token' must be dynamic. Leave 'token' for testing purpose
        key_token_param_index = hashed_token
        stdout.write("\r[*] checking {} {}".format(str(dt), hashed_token))
        stdout.flush()

        if args.method == "POST":
            # send POST request
            res = requests.post(url, data=data)
        elif args.method == "GET":
            # send GET request
            res = requests.get(url, params=data)

        # response text check        
        if (filterregex and not re.compile(args.filterregex).search(res.text)) or (matchregex and re.compile(args.matchregex).search(res.text)):
            print(res.text)
            print("[*] Congratulations! Target response printed above")
            print("Time is: "+str(dt))
            exit()
        dt += inc

def arg_parse():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-c", "--colored", action='store_true', help="let's give some random colored output")
    parser.add_argument("-d", "--data", help="insert params for GET or POST request", nargs='*', action=ParseKwargs)
    parser.add_argument("-D", "--date", help="convert a date to epoch time format")
    parser.add_argument("-div", "--divide", type=int, help="divide the timestamp by the specified value (used for change the order of magnitude)")
    parser.add_argument("-e", "--epoch", type=int, help="convert epoch time to date format")
    parser.add_argument("-f", "--float", type=float, help="deal timestamp as floating point number and specify the floating step value when range option is set")
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
    parser.add_argument("-x", "--method", default="GET", choices=["GET", "POST"], help="specify the HTTP method [default:GET]")

    args = parser.parse_args()
    return args

def main():
    args = arg_parse()

    if args.colored:
        print(colors.fg.random)

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
        token_request(args)

if __name__ == "__main__":
    main()
