#!/usr/bin/env python
# encoding: utf-8

import sys
import getopt
from fetch_impl import FetchImpl

def usage():
	print 'Usage:%s [-h | --help] [(-c | --config=) config_file'.format(sys.argv[0])

if __name__ == "__main__" :
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config="])
		if len(args) > 0:
			usage()
			sys.exit()
		config_file = 'conf/fetch_weather.conf'
		for o, a in opts:
			if o in ("-h", "--help"):
				usage()
				sys.exit()
			if o in ("-c", "--config"):
				config_file = a
	except Exception, e:
		print 'parse option exception[{}]'.format(e)
	try:
		fetch = FetchImpl(config_file)
		fetch.config()
		fetch.process()
	except Exception, e:
		sys.exit()
