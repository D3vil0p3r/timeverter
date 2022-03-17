
# TimeVerter - Time Converter Token Bruteforcer

![timeverter_screen](https://user-images.githubusercontent.com/83867734/158734970-7aa3ba3d-047d-4229-9201-6180b3b95a51.png)

**TimeVerter** helps you to bruteforce several kinds of time-based tokens and to convert several time domains.

date format: [%YYYY-%mm-%ddT%HH-%MM-%SS]\
epoch format: [seconds]

List of arguments:
| Argument | Long Argument | Input Example | Description |
| -------- | ------------- | ---------- | ----------- |
| `-c` | `--colored` | | Let's give some random colored output |
| `-d` | `--data` | param1=value param2=VERTER | Insert data for POST request (i.e. userid=user token=VERTER) |
| `-D` | `--date` | 2022-03-26T01:13:37 | Convert a date to epoch time format |
| `-div` | `--divide` | 1000 | Divide the timestamp by the specified value (used for change the order of magnitude) |
| `-e` | `--epoch` | 1647135274.789 | Convert epoch time to date format |
| `-f` | `--float` | 0.001 | Deal timestamp as floating point number and specify the floating step value when range option is set |
| `-fr` | `--filterregex` | Wrong token | Filter the response for the submitted regex |
| `-g` | `--algorithm` | sha256 | Specify the algorithm to be used for token computation |
| `-h` | `--help` | | Show this help message and exit |
| `-mr` | `--matchregex` | .\*Great.\* | Match the response for the submitted regex |
| `-mul` | `--multiply` | 1000 | Multiply the timestamp by the specified value (used for change the order of magnitude) |
| `-n` | `--now` | | Show current local time as epoch and date format |
| `-p` | `--prefix` | admin | Specify a prefix string before the timestamp |
| `-r` | `--range` | 3000 | Specify a +- offset value of the timestamp in seconds (or other magnitudes according `-div` and `-mul` options) |
| `-s` | `--suffix` | root | Specify a suffix string after the timestamp |
| `-u` | `--url` | http://x.x.x.x:XXXX | Specify the URL |
| `-U` | `--utc` | +1:00 | Show current UTC+N time as epoch and date format |
| `-v` | `--version` | | Show version information |
| `-x` | `--method` | POST | Specify the HTTP method [default:GET] |

Use `VERTER` string on the parameter to bruteforce. Choose `-n`, `-U` or `-e` option for specifying the Time Base of your attack.

Usage examples:
```
python timeverter.py -d 2022-03-26T01:13:37 -e 1647135274
python timeverter.py --utc=-3:30
python timeverter.py -U +0:00 -r 3000 -g md5 -x POST -u http://SERVER_IP:PORT/somefolder/ -d submit=check token=VERTER -fr "Wrong token" -mul 1000 -p admin
```
![timeverter_compressed](https://user-images.githubusercontent.com/83867734/158685463-03612c7d-a3ec-4ad1-8236-8d47df7cd657.gif)

# Testing
For testing it, you can set up a PHP server on your testing machine (i.e. `php -S 127.0.0.1:8000`), by using the following example PHP scripts (credits [HackTheBox](https://www.hackthebox.com/)):

**Testing by GET request**
<details>
  <summary>Click here to show the PHP file!</summary>
      
```php
<?php
// common header, can skip until READ_HERE mark
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Broken Authentication Login - Reset token time()</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script> 
<style>
	.login-form {
		width: 500px;
    	margin: 50px auto;
	}
    .login-form form {
    	margin-bottom: 15px;
        background: #f7f7f7;
        box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
        padding: 30px;
    }
    .login-form h2 {
        margin: 0 0 15px;
    }
    .form-control, .btn {
        min-height: 38px;
        border-radius: 2px;
    }
    .btn {        
        font-size: 15px;
        font-weight: bold;
    }
</style>
</head>
<body>
<div class="login-form">
<?php
// READ_HERE

// where we will save our token
$token_file = "/dev/shm/token.txt";

// if file does not exists, create a token for this test session
if (!(@file_exists($token_file))) {
  // get time in seconds
	$time = intval(microtime(true));

  // calculate token md5 hash
	$token = md5($time);

  // create and write tokenfile
  $fh = fopen($token_file, "w") or die("Unable to open file!");
  fwrite($fh, $token);
  fclose($fh);
}

// read token from file
function get_token($file) {
	$fh = fopen($file, "r");
	$token = fread($fh, filesize($file));
  // we shouldn't have any \r or \n, just to be safe
  $token = str_replace(PHP_EOL, '', $token);
	fclose($fh);
	return $token;
}

// if we have a GET as check that contain a token field, and the field is valid reply with "Great work", else just return "Wrong token"
if (isset($_GET['submit'])) {
	if ($_GET['submit'] === 'check') {
		$valid = get_token($token_file);
		if ($valid === $_GET['token']) {
			echo '<div class="alert alert-primary"> <strong>Great work!</strong></div>';
			exit;
		} else {
			echo '<div class="alert alert-warning"> <strong>Wrong token.</strong></div>';
		}
	}
}
?>
    <form action="" method="GET">
	<h2 class="text-center">Input a valid token</h2>	
        <div class="form-group">
            <input name="token" type="text" class="form-control" placeholder="Token" required="required">
        </div>

            <button value="check" name="submit" type="submit" class="btn btn-primary btn-block">Check</button>
        </div>
    </form>
</div>
</body>
</html>
```
</details>

**Testing by POST request**
<details>
  <summary>Click here to show the PHP file!</summary>
  
```php
<?php
// common header, can skip until READ_HERE mark
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Broken Authentication Login - Reset token time()</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script> 
<style>
	.login-form {
		width: 500px;
    	margin: 50px auto;
	}
    .login-form form {
    	margin-bottom: 15px;
        background: #f7f7f7;
        box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.3);
        padding: 30px;
    }
    .login-form h2 {
        margin: 0 0 15px;
    }
    .form-control, .btn {
        min-height: 38px;
        border-radius: 2px;
    }
    .btn {        
        font-size: 15px;
        font-weight: bold;
    }
</style>
</head>
<body>
<div class="login-form">
<?php
// READ_HERE

// where we will save our token
$token_file = "/dev/shm/token.txt";

// if file does not exists, create a token for this test session
if (!(@file_exists($token_file))) {
  // get time in seconds
	$time = intval(microtime(true));

  // calculate token md5 hash
	$token = md5($time);

  // create and write tokenfile
  $fh = fopen($token_file, "w") or die("Unable to open file!");
  fwrite($fh, $token);
  fclose($fh);
}

// read token from file
function get_token($file) {
	$fh = fopen($file, "r");
	$token = fread($fh, filesize($file));
  // we shouldn't have any \r or \n, just to be safe
  $token = str_replace(PHP_EOL, '', $token);
	fclose($fh);
	return $token;
}

// if we have a POST as check that contain a token field, and the field is valid reply with "Great work", else just return "Wrong token"
if (isset($_POST['submit'])) {
	if ($_POST['submit'] === 'check') {
		$valid = get_token($token_file);
		if ($valid === $_POST['token']) {
			echo '<div class="alert alert-primary"> <strong>Great work!</strong></div>';
			exit;
		} else {
			echo '<div class="alert alert-warning"> <strong>Wrong token.</strong></div>';
		}
	}
}
?>
    <form action="" method="POST">
	<h2 class="text-center">Input a valid token</h2>	
        <div class="form-group">
            <input name="token" type="text" class="form-control" placeholder="Token" required="required">
        </div>

            <button value="check" name="submit" type="submit" class="btn btn-primary btn-block">Check</button>
        </div>
    </form>
</div>
</body>
</html>
```
</details>


Use **TimeVerter** for getting the right token!\
\
\
Do you like spoilers for these tests?
<details>
  <summary>Click here to spoil!</summary>
  
  ## GET request
  `python timeverter.py -d submit=check token=VERTER -u http://127.0.0.1:8000/token_get.php -g md5 -n -fr ".*Wrong.*" -r 3000`
      
  ## POST request
  `python timeverter.py -d submit=check token=VERTER -u http://127.0.0.1:8000/token_post.php -g md5 -n -mr "G[r]ea.*" -r 3000 -x POST`
</details>

Note: in case of issues with the tests, try to remove the `/dev/shm/token.txt` generated by the PHP scripts.

