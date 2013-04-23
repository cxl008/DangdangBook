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
import threading

reload(sys)
sys.setdefaultencoding( "utf-8" )
con = None
prduct_list = []
count = 0

def Getcon():
	global con
	if con == None:
		con = sqlite3.connect('dangdang.sqlite')
	return con


def buy(product_id):
	try:
		url = "http://119.254.50.73/mobile/api.do?action=getBookInfo&&productId=%s&returnType=json&deviceType=Android&channelId=30000&clientVersionNo=2.2.1&serverVersionNo=1.1.0&activityId=0&permanentId=20130419022318537677689470094829310&deviceSerialNo=350299069409607&macAddr=cd%%3Aca%%3Aba%%3A0e%%3A37%%3A3f&resolution=320*480&clientOs=4.0.1&token=617E33E93EF4D1DEA7F3CA391B677C20jfltPi" %(product_id)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request,timeout=20)
		data =response.read()
	except:
		pass


def get_list():
	global prduct_list
	con = Getcon()
	cur = con.cursor()
	cmd = "select product_id from info"
	cur.execute(cmd)
	for item in cur.fetchall():
		id = "%s" %item
		prduct_list.append(id)
	cur.close()
	con.close()
	return prduct_list

def getproductId():
	global prduct_list
	if len(prduct_list) == 0:
		return None
	product_id = prduct_list.pop(0)
	return product_id



class Buyer(threading.Thread):  
	def __init__(self,num):  
		threading.Thread.__init__(self)  
		self.t_num = num

	def run(self):  
		while True:  
			global count
			product_id = getproductId()
			
			if product_id == None:
				break
			buy(product_id)
			count  += 1
			print "buyer  %s   %s   %s"  %(self.t_num,product_id,count)

def begin_to_buy(n):
	thread_list = []
	for i in range(n):
		thread_list.append(Buyer(i))
	for buy in thread_list:
		buy.start()


if __name__ == "__main__":
	get_list()
	begin_to_buy(5)

