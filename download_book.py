#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import urllib 
import urllib2 
import cookielib 
import string 
import zipfile 
import os,sys
import sqlite3,datetime,time,hashlib,random,chardet
from optparse import OptionParser
import base64

con = None

def Getcon():
	global con
	if con == None:
		con = sqlite3.connect('dangdang.sqlite')
	return con



def getWEBinfo(url):
	print url
	request = urllib2.Request(url)
	response = urllib2.urlopen(request,timeout=20)
	data =response.read()
	return data

def buy(product_id):
	url = "http://119.254.50.73/mobile/api.do?action=bindFreeBookAuthority&productId=%s&returnType=json&deviceType=Android&channelId=30000&clientVersionNo=2.2.1&serverVersionNo=1.1.0&activityId=0&permanentId=20130417110031199136837387376433564&deviceSerialNo=312147552218400&macAddr=fb%%3A49%%3A3e%%3A46%%3A46%%3A3c%%0A&resolution=320*480&clientOs=2.3.3&token=F23368C60AAD961187268348DD75BC47uDnBzA" %(product_id)
	getWEBinfo(url)

def getkey(product_id):
	url = "http://119.254.50.73/mobile/api.do?action=getFullBookCertificate&productId=%s&returnType=json&deviceType=Android&channelId=30000&clientVersionNo=2.2.1&serverVersionNo=1.1.0&activityId=0&permanentId=20130417110031199136837387376433564&deviceSerialNo=312147552218400&macAddr=fb%%3A49%%3A3e%%3A46%%3A46%%3A3c%%0A&resolution=320*480&clientOs=2.3.3&token=F23368C60AAD961187268348DD75BC47uDnBzA" %(product_id)
	key = getWEBinfo(url)
	return key

def download(product_id):
	url = "http://119.254.50.73/mobile/api.do?action=getBookFile&productId=%s&returnType=json&deviceType=Android&channelId=30000&clientVersionNo=2.2.1&serverVersionNo=1.1.0&activityId=0&permanentId=20130417110031199136837387376433564&deviceSerialNo=312147552218400&macAddr=fb%%3A49%%3A3e%%3A46%%3A46%%3A3c%%0A&resolution=320*480&clientOs=2.3.3&token=F23368C60AAD961187268348DD75BC47uDnBzA" %(product_id)
	content = getWEBinfo(url)
	if content == "{\"statusCode\":1,\"errorCode\":-1003}":
		buy(product_id)
	content = getWEBinfo(url)
	basename = "%s.epub" %product_id
	bookpath = os.path.join("book",basename)
	f = open(bookpath,'w')
	f.write(content)
	f.close()

if __name__ == "__main__":
	con = Getcon()
	cur = con.cursor()
	cur_insert = con.cursor()
	cmd = "select name,product_id from info limit 2"
	cur.execute(cmd)
	for name,product_id in cur.fetchall():
		download(product_id)
		print product_id

