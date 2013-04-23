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
from beautiful_soup import BeautifulSoup as bs


reload(sys)
sys.setdefaultencoding( "utf-8" )

con = None

def Getcon():
	global con
	if con == None:
		con = sqlite3.connect('dangdang.sqlite')
	return con

def insert(title,product_id):
	title = title.replace("\'",' ')
	print title,product_id
	con = Getcon()
	cur = con.cursor()
	cmd = "select * from info where product_id='%s'" %product_id
	cur.execute(cmd)
	info =  cur.fetchone()
	if info == None:
		cmd = "insert into info(name,product_id) values('%s','%s')" %(title,product_id)
		cur.execute(cmd)
		cur .close()
		con.commit()
		buy(product_id)


def praseRefer(content):

	soup = bs(content)

	for item in soup.findAll("div",{"class":"ebookLst_s"}):
		for ii in item.findAll("div",{"class":"con"}):
			jj = ii.findChildren()

			link =  jj[1].get('href')
			product_id = link.replace("http://product.dangdang.com/product.aspx?product_id=",'')
			name = jj[1].text
			try:
				insert(name,product_id)
			except:
				pass


def getWEBinfo(url):

	request = urllib2.Request(url)
	response = urllib2.urlopen(request,timeout=20)
	data =response.read()
	return data

def buy(product_id):
	url = "http://119.254.50.73/mobile/api.do?action=bindFreeBookAuthority&productId=%s&returnType=json&deviceType=Android&channelId=30000&clientVersionNo=2.2.1&serverVersionNo=1.1.0&activityId=0&permanentId=20130417110031199136837387376433564&deviceSerialNo=312147552218400&macAddr=fb%%3A49%%3A3e%%3A46%%3A46%%3A3c%%0A&resolution=320*480&clientOs=2.3.3&token=F23368C60AAD961187268348DD75BC47uDnBzA" %(product_id)
	request = urllib2.Request(url)
	response = urllib2.urlopen(request,timeout=20)
	data =response.read()

if __name__ == "__main__":
	for bigcode in ['03','52','05','01','21','41','10','30','22.03','43','58']:

		for code in range(1,150):
			url= "http://e.dangdang.com/list_98.01.%s_%s_saleWeek_1.htm" %(bigcode,code)
			print url 
			data = getWEBinfo(url)
			praseRefer(data)
			time.sleep(0.5)


