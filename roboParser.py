#!/usr/bin/env python


import sys
import urllib2
import argparse

def parse(urlBase):

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
			print str(robResp.code) + " -- " + item + " -- " + str(robResp.headers['content-length'])
			#print "----------"
			#print robResp.read()
			#print " -----------"
	
		except urllib2.HTTPError as e:
				print str(e.code) + " -- " + item	

if __name__ == "__main__":


	parser = argparse.ArgumentParser(description="Check response codes and sizes for paths listed in a baseURL's robots.txt")
	parser.add_argument('URL', metavar= 'URL', type=str, nargs=1)
	parser.add_argument("-d", metavar='delay', type=int, nargs=1, help="Delay in milliseconds")
	
	args = parser.parse_args()

	url = args.URL.pop()
	delay = args.d.pop()

	parse(url)
