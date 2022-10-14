import base64, zlib
import src.time as verter

############################################################
# Help                                                     #
############################################################
def help():
   # Display Help
   print_version()
   print("TimeVerter helps you to bruteforce several kinds of time-based tokens and to convert several time domains.\n")
   
   print("date format: [%YYYY-%mm-%ddT%HH:%MM:%SS]")
   print("epoch format: [seconds]\n")

   print("List of arguments:\n")
   
   print("-c, --colored                 let's give some random colored output")
   print("-d, --data <data>             insert data for POST request (i.e. userid=user token=VERTER)")
   print("-D, --date <date>             convert a date to epoch time format")
   print("-div, --divide <N>            divide the timestamp by the specified value (used for change the order of magnitude)")
   print("-e, --encode <pattern>        encode the input to a chain of the specified formats. It will be applied before the --algorithm option")
   print("-E, --epoch <seconds>         convert epoch time to date format")
   print("-f, --float <N>               deal timestamp as floating point number and specify the floating step value when range option is set")
   print("-fr, --filterregex <pattern>  filter the response for the submitted regex")
   print("-g, --algorithm <algorithm>   specify the algorithm to be used for token computation (look for hashlib or OpenSSL algorithms)")
   print("-h, --help                    show this help message and exit")
   print("-H, --header                  specify the headers of the request")
   print("-mr, --matchregex <pattern>   match the response for the submitted regex")
   print("-mul, --multiply <N>          multiply the timestamp by the specified value (used for change the order of magnitude)")
   print("-n, --now                     show current local time as epoch and date format")
   print("-p, --prefix <pattern>        specify a prefix string before the timestamp")
   print("-r, --range <N>               specify a +- offset value of the timestamp in seconds (or other magnitudes according -div and -mul options)")
   print("-s, --suffix <pattern>        specify a suffix string after the timestamp")
   print("-u, --url <URL>               specify the URL")
   print("-U, --utc <time>              show current UTC+N time as epoch and date format")
   print("-v, --verbose                 show verbose output")
   print("-V, --version                 show version information")
   print("-X, --request <method>        specify request method to use")
   print("-z, --compare <pattern>       compare a value to the output tokens")
   print("\n")
   print("Use VERTER string on the parameter to bruteforce. Choose -n, -U or -E option for specifying the Time Base of your attack.")
   print("\n")
   print("Usage Examples:")
   print("timeverter -D 2022-03-26T01:13:37")
   print("timeverter --utc=-3:30")
   print("timeverter -n -g md5 -r 3000 -z a4e11f213f0bc314a043207dba6ca8ca")
   print("timeverter -U +0:00 -r 3000 -g md5 -x POST -u http://SERVER_IP:PORT/somefolder/ -d submit=check token=VERTER -fr \"Wrong token\" -mul 1000 -p admin")
   print("timeverter -u 'http://SERVER_IP:PORT/somefolder/' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Connection: keep-alive' -H 'Cookie: SESSIONID=VERTER' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' -n -e b64,hex -v -X GET -r 1000")

def print_banner():
    #cat banner.txt | gzip | base64
    encoded_data = "H4sIAAAAAAAAA11RW47DIAz85xTzR5Aas7S7bbc5xF4AyRwkh68fQJM1ssEzFhgPoMZuOFmwmFnphZPyVqPBOeS+BGniVU6o4UR9llTl4FdmdY/qlQc1zNr5IEzRkEYTpEhrBMoVbaVGo6FLRCl+Lmg0mskoX6Nl4IrqxLbNJ3LfXy9j9h2/wCr25/hNoOAF+G/b5s/UiucB/pZ3e1+1ER4d/sElzt9GkvaZ78zyHYrzy8uiMCuc0kQ5pcnPScRVBzGPAewTPE7z0FXYsZs8XUs2DXhmxpuopqfS5iNTfsipm6s4Mr1fq0xSxVFPmfDhDQApq7V0AgAA"
    banner = zlib.decompress(base64.b64decode(encoded_data), 16 + zlib.MAX_WBITS).decode('utf-8')
    print(banner)

def print_version():
    print_banner()
    print("TimeVerter v1.3.0")

def print_settings(args):
    print_version()
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
        tb = ''.join(["Epoch Time: ",str(args.epoch),"; Date Time: ", verter.epoch_to_date(args.epoch)])
    if args.now or args.utc or args.epoch:
        print("[*] Time Base             : %s" % tb)
    if args.range:
        print("[*] Time Range            : %s" % args.range)
    if args.multiply:
        print("[*] Time Multiply Factor  : %d" % args.multiply)
    if args.divide:
        print("[*] Time Divide Factor    : %d" % args.divide)
    if args.encode:
        print("[*] Encoding              : %s" % args.encode)
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
    if args.compare:
        print("[*] Comparing String      : %s" % args.compare)
    print("________________________________________________")
    print("")
