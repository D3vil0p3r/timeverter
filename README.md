# TimeVerter
```
      _______              
     /_  __(_)___ ___  ___ 
      / / / / __ `__ \/ _ \
     / / / / / / / / /  __/
    /_/ /_/_/ /_/ /_/\___/
            _____
         _.'_____`._
       .'.-'  12 `-.`.
      /,' 11      1 `.\
     // 10      /   2 \\
    ;;         /       ::
    || 9  ----O      3 ||
    ::                 ;;
     \\ 8           4 //
      \`. 7       5 ,'/
       '.`-.__6__.-'.'
        ((-._____.-))
        _))       ((_
       '--'       '--'
 _    __          __           
| |  / /__  _____/ /____  _____
| | / / _ \/ ___/ __/ _ \/ ___/
| |/ /  __/ /  / /_/  __/ /    
|___/\___/_/   \__/\___/_/     


Timeverter helps you to convert several time domains and to bruteforce several kinds of tokens.

syntax: timeverter.py [-d DATE] [-e EPOCH] [-h]

date format: [%YYYY-%mm-%ddT%HH-%MM-%SS]
epoch format: [seconds]

optional arguments:

-d DATA, --data DATA        insert data for POST request (i.e. userid=user token=VERTER)
-D DATE, --date DATE        convert a date to epoch time format
-div N, --divide N          divide the timestamp by the specified value (used for change the order of magnitude)
-e EPOCH, --epoch EPOCH     convert epoch time to date format
-f, --float                 deal timestamp as floating point number
-fr, --filterregex PATTERN  filter the response for the submitted regex
-g, --algorithm             specify the algorithm to be used for token computation
-h, --help                  show this help message and exit
-mr, --matchregex PATTERN   match the response for the submitted regex
-mul, --multiply N          multiply the timestamp by the specified value (used for change the order of magnitude)
-n, --now                   show current local time as epoch and date format
-p, --prefix PATTERN        specify a prefix string before the timestamp
-r, --range N               specify a +- offset value of the timestamp in seconds (or other magnitudes according -div and -mul options)
-s, --suffix PATTERN        specify a suffix string after the timestamp
-u, --url URL               specify the url
-U, --utc TIME              show current UTC+N time as epoch and date format


Usage examples:
python timeverter.py -d 2022-03-26T01:13:37 -e 1647135274
python timeverter.py --utc=-3:30
python timeverter.py -U +0:00 -r 3000 -g md5 -u http://SERVER_IP:PORT/somefolder/ -d submit=check token=VERTER -fr "Wrong token" -mul 1000 -p admin
```
