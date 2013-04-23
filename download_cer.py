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

	request = urllib2.Request(url)
	response = urllib2.urlopen(request,timeout=20)
	data =response.read()
	return data

def getkey(product_id):
	url = "http://119.254.50.73/mobile/api.do?action=getFullBookCertificate&productId=%s&returnType=json&deviceType=Android&channelId=30000&clientVersionNo=2.2.1&serverVersionNo=1.1.0&activityId=0&permanentId=20130417110031199136837387376433564&deviceSerialNo=312147552218400&macAddr=fb%%3A49%%3A3e%%3A46%%3A46%%3A3c%%0A&resolution=320*480&clientOs=2.3.3&token=F23368C60AAD961187268348DD75BC47uDnBzA" %(product_id)
	key = getWEBinfo(url)
	return key

def download(product_id):
	url = "http://119.254.50.73/mobile/api.do?action=getBookFile&productId=%s&returnType=json&deviceType=Android&channelId=30000&clientVersionNo=2.2.1&serverVersionNo=1.1.0&activityId=0&permanentId=20130417110031199136837387376433564&deviceSerialNo=312147552218400&macAddr=fb%%3A49%%3A3e%%3A46%%3A46%%3A3c%%0A&resolution=320*480&clientOs=2.3.3&token=F23368C60AAD961187268348DD75BC47uDnBzA" %(product_id)
	content = getWEBinfo(url)
	bookpath = os.path.join("book",product_id)
	f = file(bookpath,'w')
	f.write(content)
	f.close()

if __name__ == "__main__":
	con = Getcon()
	cur = con.cursor()
	cur_insert = con.cursor()
	cmd = "select name,product_id from info where key is null"
	cur.execute(cmd)
	for name,product_id in cur.fetchall():
		key = getkey(product_id)
		key = base64.b64encode(key)
		print product_id
		cmd= "update info set key='%s' where product_id='%s" %(key,product_id)
		cur_insert.execute(cmd)
		con.commit()

