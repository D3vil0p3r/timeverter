import requests
import hashlib
from .parser import arg_parse
from .util import colors
from .util import check_url
import src.time as verter
import src.printer as printer

from sys import stdout
import re

def define_time(now_time,utc_time,epoch_time,mul,div):
    if now_time:
        ts = verter.current_local_epoch()
    elif utc_time:
        ts = verter.current_utc_epoch(utc_time)
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
    printer.print_settings(args)
    
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

def main():
    args = arg_parse()

    if args.colored:
        print(colors.fg.random)

    if args.help:
        printer.help()

    if args.now and not args.algorithm:
        print("Date time  [local time]: "+str(verter.current_local_date()))
        print("Epoch time [local time]: "+str(verter.current_local_epoch())) #The output is a little skewed because the two functions are called in two different times

    if args.utc and not args.algorithm:
        print("Date time  [UTC%s]: " % args.utc +str(verter.current_utc_date(args.utc)))
        print("Epoch time [UTC%s]: " % args.utc +str(verter.current_utc_epoch(args.utc)))

    if args.date and not args.algorithm:
        print("Epoch time: "+str(verter.date_to_epoch(args.date)))

    if args.epoch and not args.algorithm:
        print("Date time:  "+verter.epoch_to_date(args.epoch))

    if args.url:
        token_request(args)