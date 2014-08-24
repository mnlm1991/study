#!/usr/bin/env python
#-*- coding: utf-8 -*-
#########################################################################
# Author: penggongkui
# Created Time: 2014-08-23 23:54:19
# File Name: fetch_impl.py
# Description: 
#########################################################################

# vim: set noexpandtab ts=4 sts=4 sw=4 :

import urllib2
import json
import string
import logging
import logging.config
import ConfigParser
import sys

sys.path.append('../thrift_weather_CS/gen-py/')

from thrift.transport.TTransport import TFileObjectTransport
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

from weatherCS.ttypes import weather_info

class FetchImpl:
	
	def __init__(self, config_file) :
		self.config_file = config_file	# 配置文件
		self.city_list = []				# 抓取的城市列表
	
	@staticmethod
	def splitInt(str):
		i = 0
		while i < len(str):
			if str[i] < '0' or str[i] > '9':
				break
			i = i + 1
		return int(str[0:i])
	
	@staticmethod
	def isCityId(id):
		"""
			判断天气ID是否合理
		"""
		for i in id:
			if i < '0' or i > '9':
				return False
		return True
	
	def getCityId(self, weather_info):
		return weather_info[self.weather_key][self.city_id_key]
	
	def getCityName(self, weather_info):
		return weather_info[self.weather_key][self.city_name_key]
	
	def getMaxTemp(self, weather_info):
		return self.splitInt(weather_info[self.weather_key][self.max_temp_key])
	
	def getMinTemp(self, weather_info):
		return self.splitInt(weather_info[self.weather_key][self.min_temp_key])
	
	def readCity(self):
		"""
			从配置文件中读取要抓取天气的城市
		"""
		try:
			log = logging.getLogger('weather')
			file = open(self.data_conf, 'r')
			for line in file.readlines():
				line = line.strip('\n')
				if self.isCityId(line):
					self.city_list.append(line)
					log.debug('city_id[{}] added to fetch list'.format(line))
				else:
					log.warn('{} is not invalid city_id'.format(line))
			file.close()
		except Exception, e:
			log.fatal('read_city exception[{}]'.format(e))
	
	def config(self):
		"""
			读取配置文件，并做一些初始化
		"""
		try:
			cf = ConfigParser.ConfigParser()
			cf.read(self.config_file)
			log_config = cf.get('log', 'config')
			logging.config.fileConfig(log_config)
			self.fetch_url = cf.get("site", "url")
			self.city_id_key = cf.get('site', 'city_id_key')
			self.city_name_key = cf.get('site', 'city_name_key')
			self.max_temp_key = cf.get('site', 'max_temp_key')
			self.min_temp_key = cf.get('site', 'min_temp_key')
			self.weather_key = cf.get('site', 'weather_key')
			self.url_ext = cf.get('site', 'url_ext')
			self.data_conf = cf.get('data', 'config')
			self.readCity()
			self.data_file = cf.get('data', 'file')
		except Exception, e:
			print 'config exception: [{}]'.format(e)
			raise e
	
	def process(self):
		"""
			进行天气的抓取
		"""
		log = logging.getLogger('weather')
		try:
			f = open(self.data_file, "w")
			trans = TFileObjectTransport(f)
			trans = TBufferedTransport(trans)
			proto = TBinaryProtocol(trans)
			trans.open()
		except Exception, e:
			log.fatal('process.open file exception [{}]'.format(e))
			trans.close()
			f.close()
			raise e
		for city in self.city_list:
			url = self.fetch_url + city + self.url_ext
			try:
				content = urllib2.urlopen(url).read()
				weather = json.loads(content)
				info = weather_info(self.getCityId(weather), self.getCityName(weather), self.getMaxTemp(weather), self.getMinTemp(weather))
				info.write(proto)
			except Exception, e:
				log.warn('fetch url[{}] exception [{}]'.format(url, e))

		trans.flush()
		trans.close()
		f.close()
