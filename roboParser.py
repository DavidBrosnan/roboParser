#!/usr/bin/env python


import sys
import urllib2
import argparse
import time

def parse(urlBase, delay, ignore):

	urlRobots = urlBase + "/robots.txt"	
	resp = urllib2.urlopen(urlRobots).readlines()
	pathList = []
	

	for line in resp:
		if "Disallow:" in line or "Allow:" in line:
			pathList.append(line[line.index("/"):-1:])

	for item in pathList:
		url = urlBase + item	
		robResp = "XXX"
			
		try:
			robResp = urllib2.urlopen(url)
			print "{0:3} -- {1:40} -- {2:5}".format(robResp.code, item, str(robResp.headers['content-length']))
	
		except urllib2.HTTPError as e:
			if not ignore:	
				print "{0:3} -- {1:40} -- {2:5}".format(e.code, item, str(e.headers['content-length']))

		time.sleep(delay/1000)


if __name__ == "__main__":


	parser = argparse.ArgumentParser(description="Check response codes and sizes for paths listed in a baseURL's robots.txt")
	parser.add_argument('URL', metavar= 'URL', type=str, nargs=1)
	parser.add_argument("-d", metavar='delay', type=int, nargs=1, help="Delay in milliseconds")
	parser.add_argument("--ignore", action='store_true', help="Ignore 4xx and 5xx response codes")	

	args = parser.parse_args()

	url = args.URL.pop()
	
	if args.d is not None:
		delay = args.d.pop()
	else:
		delay = 0

	if args.ignore is not None:
		ignore = args.ignore
	else:
		ignore = False

	parse(url, delay, ignore)
