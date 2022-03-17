import base64, zlib

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
   
   print("-c, --colored                 let's give some random colored output")
   print("-d, --data <data>             insert data for POST request (i.e. userid=user token=VERTER)")
   print("-D, --date <date>             convert a date to epoch time format")
   print("-div, --divide <N>            divide the timestamp by the specified value (used for change the order of magnitude)")
   print("-e, --epoch <seconds>         convert epoch time to date format")
   print("-f, --float <N>               deal timestamp as floating point number and specify the floating step value when range option is set")
   print("-fr, --filterregex <pattern>  filter the response for the submitted regex")
   print("-g, --algorithm <algorithm>   specify the algorithm to be used for token computation (look for hashlib or OpenSSL algorithms)")
   print("-h, --help                    show this help message and exit")
   print("-mr, --matchregex <pattern>   match the response for the submitted regex")
   print("-mul, --multiply <N>          multiply the timestamp by the specified value (used for change the order of magnitude)")
   print("-n, --now                     show current local time as epoch and date format")
   print("-p, --prefix <pattern>        specify a prefix string before the timestamp")
   print("-r, --range <N>               specify a +- offset value of the timestamp in seconds (or other magnitudes according -div and -mul options)")
   print("-s, --suffix <pattern>        specify a suffix string after the timestamp")
   print("-u, --url <URL>               specify the URL")
   print("-U, --utc <time>              show current UTC+N time as epoch and date format")
   print("-v, --version                 show version information")
   print("-X, --request <method>        specify request method to use")
   print("\n")
   print("Use VERTER string on the parameter to bruteforce. Choose -n, -U or -e option for specifying the Time Base of your attack.")
   print("\n")
   print("Usage examples:")
   print("python timeverter.py -d 2022-03-26T01:13:37 -e 1647135274")
   print("python timeverter.py --utc=-3:30")
   print("python timeverter.py -U +0:00 -r 3000 -g md5 -x POST -u http://SERVER_IP:PORT/somefolder/ -d submit=check token=VERTER -fr \"Wrong token\" -mul 1000 -p admin")

def print_banner():
    #cat banner.txt | gzip | base64
    encoded_data = "H4sIAAAAAAAAA11RW47DIAz85xTzR5Aas7S7bbc5xF4AyRwkh68fQJM1ssEzFhgPoMZuOFmwmFnphZPyVqPBOeS+BGniVU6o4UR9llTl4FdmdY/qlQc1zNr5IEzRkEYTpEhrBMoVbaVGo6FLRCl+Lmg0mskoX6Nl4IrqxLbNJ3LfXy9j9h2/wCr25/hNoOAF+G/b5s/UiucB/pZ3e1+1ER4d/sElzt9GkvaZ78zyHYrzy8uiMCuc0kQ5pcnPScRVBzGPAewTPE7z0FXYsZs8XUs2DXhmxpuopqfS5iNTfsipm6s4Mr1fq0xSxVFPmfDhDQApq7V0AgAA"
    banner = zlib.decompress(base64.b64decode(encoded_data), 16 + zlib.MAX_WBITS).decode('utf-8')
    print(banner)

def print_version():
    print_banner()
    print("TimeVerter v1.2.0")

def print_settings(args):
    print_banner()
    print("________________________________________________")
    print("")
    if args.request:
        print("[*] Method                : %s" % args.request)
    if args.url:
        print("[*] URL                   : %s" % args.url)
    if args.data:
        print("[*] Parameters            : %s" % args.data)
    if args.now:
        tb = "Current Local Time"
    elif args.utc:
        tb = ''.join(["Current UTC",args.utc," Time"])
    elif args.epoch:
        tb = ''.join(["Epoch Time: ",str(args.epoch),"; Date Time: ",epoch_to_date(args.epoch)])
    if args.now or args.utc or args.epoch:
        print("[*] Time Base             : %s" % tb)
    if args.range:
        print("[*] Time Range            : %s" % args.range)
    if args.multiply:
        print("[*] Time Multiply Factor  : %d" % args.multiply)
    if args.divide:
        print("[*] Time Divide Factor    : %d" % args.divide)
    if args.algorithm:
        print("[*] Algorithm             : %s" % args.algorithm)
    if args.prefix:
        print("[*] Prefix                : %s" % args.prefix)
    if args.suffix:
        print("[*] Suffix                : %s" % args.suffix)
    if args.matchregex:
        print("[*] Matcher               : regexp -> %s" % args.matchregex)
    if args.filterregex:
        print("[*] Filter                : regexp -> %s" % args.filterregex)
    if args.float:
        print("[*] Float Step value      : %f" % args.float)
    print("________________________________________________")
    print("")
