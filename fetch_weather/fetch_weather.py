#!/usr/bin/env python
# encoding: utf-8

from fetch_impl import FetchImpl

if __name__ == "__main__" :
	try:
		fetch = FetchImpl('fetch_weather.conf')
		fetch.config()
		fetch.process()
	except Exception, e:
		sys.exit()
