import argparse, requests, sys, logging

parser = argparse.ArgumentParser(add_help = True, description = "This is a simple easy to use web fuzzer")
parser.add_argument("-m", action="store", help="Mode to use: dir or fuzz")
parser.add_argument("-u", action="store", help="URL to target; i.e. http://192.168.1.1/")
parser.add_argument("-w", action="store", help="Path to the wordlist to use: i.e. /usr/share/wordlists/rockyou.txt")
parser.add_argument("--method", action="store", default="GET", help="Method to use in the requests; GET by default, note that it's key-sensitive")
parser.add_argument("-p", action="store", help= "Parameter to use during fuzzing; i.e parameter1")

if len(sys.argv) == 1:
	parser.print_help()
	sys.exit(1)
try:
	options = parser.parse_args()
except Exception as e:
	logging.critical(str(e))
	sys.exit(1)

if options.m == "dir":
	with open(options.w, 'r') as f:
		for word in f:
			url = options.u + word.rstrip()
			s = requests.Session()
			if options.method == "POST":
				r = s.post(url=url)
				if r.status_code == 404:
					pass
				else:
					print("[+] " + str(r.status_code) + " -> " + url)
			else:
				r = s.get(url=url)
				if r.status_code == 404:
					pass
				else:
					print("[+] " + str(r.status_code) + " -> " + url)

elif options.m == "fuzz":
	with open(options.w, 'r') as f:
		for word in f:
			s = requests.Session()
			if options.method == "GET":
				url = options.u + "?" + options.p + "=" + word.rstrip()
				r = s.get(url=url)
				if r.status_code == 404:
					pass
				else:
					print("[+] " + str(r.status_code) + " -> " + url)
			elif options.method == "POST":
				url = options.u
				data = {options.p : word.rstrip()}
				r = s.post(url=url, data=data)
				if r.status_code == 404:
					pass
				else:
					print("[+] " + str(r.status_code) + " -> " + options.p + ":" + word.strip())
			else:
				print("[+] Please enter a valid method!")
				sys.exit(1)
else:
	print("[+] Please select a valid mode!")


	