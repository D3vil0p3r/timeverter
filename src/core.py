import requests
import hashlib
import base64
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

def encode_chain(enc,str_in):
    enc_list = enc.split(",")
    str_res = str_in
    for x in enc_list:
        if x == "base64" or x == "b64":
            str_bytes = str_res.encode("ascii")
            str_res = base64.b64encode(str_bytes).decode("ascii")
        elif x == "hex" or x == "hexadecimal":
            str_res = str_res.encode("utf-8").hex()
        #Add other encodings...
    return str_res

def compute_token(alg,enc,ts,prefix,suffix):
    token = str(ts)
    if not alg and not enc:
        print ("Error! Specify an algorithm or an encoding format.")
        exit()
    else:
        if enc:
            token = encode_chain(enc,token)
        if alg:
            h = hashlib.new(alg)
            h.update(''.join([prefix, token, suffix]).encode('utf-8'))
            token = h.hexdigest()

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
    enc = args.encode
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

    headers = {}
    if args.header:
        # Extract headers
        for header in args.header:
            name, _, value = header.partition(': ')
            headers[name] = value
    
    data = args.data
    
    #Check if headers and data contain VERTER string
    check_headers = [y for x, y in headers.items() if key_token_param_index in y]
    check_data = [y for x, y in data.items() if key_token_param_index in y]

    dt = ts - rng
    while dt <= ts + rng:
        hashed_token = compute_token(alg,enc,dt,prefix_str,suffix_str)
        
        if args.header and check_headers:
            head_value = [y for x, y in headers.items() if key_token_param_index in y][0]
            start_value = head_value.replace(key_token_param_index,'') #Manage case where VERTER is a substring (i.e., Cookie: SESSIONID=VERTER)
            headers[list(headers.keys())[list(headers.values()).index(head_value)]] = start_value + hashed_token
        
        
        if args.data and check_data:
            data[list(data.keys())[list(data.values()).index(key_token_param_index)]] = hashed_token #'token' must be dynamic. Leave 'token' for testing purpose
        key_token_param_index = hashed_token
        stdout.write("\r[*] checking {} {}".format(str(dt), hashed_token))
        stdout.flush()

        if args.request == "POST":
            # send POST request
            res = requests.post(url, data=data, headers=headers)
        elif args.request == "GET":
            # send GET request
            res = requests.get(url, params=data, headers=headers)
        if args.verbose:    
            print("\n")
            print("\n".join("{}: {}".format(k, v) for k, v in res.request.headers.items()))
            print("\n")
            print(res.request.body)
            print("\n")
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

    if args.version:
        printer.print_version()

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
        if args.request:
            token_request(args)
        else:
            print("Error! Please specify a HTTP method [GET or POST]")
