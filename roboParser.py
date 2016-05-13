#!/usr/bin/env python


import sys
import urllib2
import argparse
import time

class RedirectHandler(urllib2.HTTPRedirectHandler):
	
	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
		result.status = code
		return result
	http_error_301 = http_error_303 = http_error_307 = http_error_302

def getSize(httpResp):
	try:
		contentSize = httpResp.headers['content-length']
		return contentSize
	except KeyError as e:
		headers = httpResp.headers.keys()
		if 'transfer-encoding' in headers and 'content-length' not in headers:
			if httpResp.headers['transfer-encoding'] == 'chunked':
				return "Chunked"	
		return "ERROR"

def parse(urlBase, delay, ignore):

	urlRobots = urlBase + "/robots.txt"	
	resp = urllib2.urlopen(urlRobots).readlines()
	pathList = []
	opener = urllib2.build_opener(RedirectHandler())

	for line in resp:
		if ("Disallow:" in line or "Allow:" in line) and "/" in line:
			slash = line.index("/")
			try:	
				pathList.append(line[slash:-1:])

			except ValueError as e:
				print "Error Parsing: " + line

	for item in pathList:
		url = urlBase + item	
		robResp = "XXX"
			
		try:
			robResp = opener.open(url)
		
			print "{0:3} -- {1:40} -- {2:5}".format(robResp.code, item, getSize(robResp))
			
			if robResp.code == 301 or robResp.code == 302 or robResp.code == 303 or robResp.code == 307:
				robResp2 = urllib2.urlopen(robResp.headers['location'])
				print "    Redirect --> {0:3} -- {1:40} -- {2:5}".format(robResp2.code, robResp2.geturl(), getSize(robResp2))
			
	
		except urllib2.HTTPError as e:
			if not ignore:	
				print "{0:3} -- {1:40} -- {2:5}".format(e.code, item, getSize(e))

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
