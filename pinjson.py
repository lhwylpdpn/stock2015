#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import os
import math
import scipy.stats
import time
import random
import mail

def clac1(a,b,c):
	p=a
	OneP=b
	bucang=c
	kongjian=[3,6,11,19,32,53,87,142,231,375,608]
	i=0
	sumall=0
	for n in kongjian:
		
		sumall=sumall+(1-OneP)*pow((1-p),i)*n*bucang
		i=i+1

	return p*bucang/6-sumall



def readsql():
	line=[]
	open_=[]
	open_noclose=[]
	norm_=[]
	norm_cha=[]
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_llllllllllllmx',port=3306)
	cur_stock=conn.cursor()
	sql="SELECT CONCAT('[',UNIX_TIMESTAMP(DATE_FORMAT(CONCAT(DATE,' ',TIME),'%Y.%m.%d %H:%i')),'000,',CLOSE,']') FROM `stock` WHERE stockid='GBPAUD.lmx';"
	sql2="SELECT CONCAT('[',UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000',']') FROM `order` a , `order_result` b WHERE a.stockid ='GBPAUD.lmx' AND a.`orderid`=b.`ln_e_close`"
	sql3="SELECT CONCAT('[',UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000',']') FROM `order` a  WHERE a.stockid ='GBPAUD.lmx' AND a.`orderid` NOT IN (SELECT ln_e_close FROM order_result)"
	sql4="SELECT CONCAT('[',UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000,',a.`norm_open`,']') FROM `order` a WHERE a.stockid ='GBPAUD.lmx'"
	sql5="SELECT CONCAT('[',UNIX_TIMESTAMP(DATE_FORMAT(a.order_time_send,'%Y-%m-%d %H:%i')),'000,',a.`norm_cha_open`,']') FROM `order` a  WHERE a.stockid ='GBPAUD.lmx'"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	for r in res:
		line.append(str(r[0]))

	cur_stock.execute(sql2)
	res=cur_stock.fetchall()
	for r in res:
		open_.append(str(r[0]))

	cur_stock.execute(sql3)
	res=cur_stock.fetchall()
	for r in res:
		open_noclose.append(str(r[0]))


	cur_stock.execute(sql4)
	res=cur_stock.fetchall()
	for r in res:
		norm_.append(str(r[0]))

	cur_stock.execute(sql5)
	res=cur_stock.fetchall()
	for r in res:
		norm_cha.append(str(r[0]))

	writle_json(line,open_,open_noclose,norm_,norm_cha)

def writle_json(line,open_,open_noclose,norm_,norm_cha):
	file_object = open('json/test_GBPAUD.json','w')
	file_object.write('[')
	for r in range(0,len(line)):
		if r!=len(line)-1:
			
			file_object.write(line[r]+",\n")
		else:
			file_object.write(line[r]+"]")
	file_object.close()

	file_object = open('json/test2_GBPAUD.json','w')
	file_object.write('[')
	for r in range(0,len(open_)):
		if r!=len(open_)-1:
			
			file_object.write(open_[r]+",\n")
		else:
			file_object.write(open_[r]+"]")
	file_object.close()
	
	file_object = open('json/test3_GBPAUD.json','w')
	file_object.write('[')
	for r in range(0,len(open_noclose)):
		if r!=len(open_noclose)-1:
			
			file_object.write(open_noclose[r]+",\n")
		else:
			file_object.write(open_noclose[r]+"]")
	file_object.close()


	file_object = open('json/test4_GBPAUD.json','w')
	file_object.write('[')
	for r in range(0,len(norm_)):
		if r!=len(norm_)-1:
			
			file_object.write(norm_[r]+",\n")
		else:
			file_object.write(norm_[r]+"]")
	file_object.close()

	file_object = open('test5_GBPAUD.json','w')
	file_object.write('[')
	for r in range(0,len(norm_cha)):
		if r!=len(norm_cha)-1:
			
			file_object.write(norm_cha[r]+",\n")
		else:
			file_object.write(norm_cha[r]+"]")
	file_object.close()	

if __name__ == '__main__':
	readsql()