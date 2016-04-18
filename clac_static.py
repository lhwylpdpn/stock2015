#coding:utf-8
import pymysql
import os
import time
import mail
def getInfo(processname):             #通过tasklist命令，找到processname的pid
	word1=""
	word2=""
	task = os.popen('tasklist')
	if processname in task.read():
		#print(1)
		num = os.popen('wmic process where name="'+processname+'" get CommandLine')
		#print( num.read().split("\n"))
		#print(num.read().split("\n")[2].index("E:\BaiduYunDownload\phpStudy\WWW\\forlining\\task.py"))
		for r in num.read().split("\n"):
			if r.strip()!='':

				word="E:\BaiduYunDownload\phpStudy\WWW\\forlining\\task.py"
				if r.find("C:\github\stock2015\process_1.2.py")!=-1:
					word1=',"jiasheng_status":1'
				# if r.find("C:\github\stock2016forlmx\process_1.2_forlmx.py")!=-1:
				# 	word2=',"lmx_status":1'
	if word1=="":
		word1=',"jiasheng_status":0'
		writelog("停止了")
		mail.run("mail.ini","警报！！！,程序断掉了"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))

	if word2=="":
		word2=',"lmx_status":0'		
		# writelog("停止了")
		# mail.run("mail.ini","警报！！！,lmx程序断掉了"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))

	write_json(word1+word2)

def writelog(str):
	file=open("mail.ini","a")
	file.write(str+"\n")
	file.close()	

def  clac_json():
	avg_num=[]
	word3=""
	conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	cur_stock=conn.cursor()
	sql="SELECT AVG(b) FROM (SELECT STR_TO_DATE(order_time_send,'%Y-%c-%d') AS a,COUNT(*) AS b FROM `order` GROUP BY STR_TO_DATE(order_time_send,'%Y-%c-%d') HAVING a>DATE_ADD(now(),INTERVAL -7 DAY)) a"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	for r in res:
		word1=str(r[0])

	sql="SELECT SUM(CASE WHEN  lots_A=0.01 THEN 1 END )/COUNT(*) FROM `order_result`   "
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	for r in res:
		word2=str(r[0])
	
	sql="SELECT SUM(CASE WHEN  lots_A=0.01 THEN orderid END )/sum(orderid) FROM `order_result`    "
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	for r in res:
		word4=str(r[0])


	word3=""
	# sql="SELECT nameA,SUM(CASE WHEN lots_A=0.01 THEN 1 END) AS a ,SUM(CASE WHEN lots_A=0.01 THEN 1 END)/COUNT(*) AS b,MAX(lots_A) c,AVG(CASE WHEN lots_A=0.01 THEN TIMESTAMPDIFF(MINUTE,openA_time,closeA_time) END) AS d,AVG(CASE WHEN lots_A<>0.01 THEN TIMESTAMPDIFF(MINUTE,openA_time,closeA_time) END) AS e ,ROUND(SUM(CASE WHEN lots_A=0.01 THEN orderid END),2) AS f,ROUND(SUM(CASE WHEN lots_A<>0.01 THEN orderid END),2) AS g FROM order_result   GROUP BY nameA;"
	# cur_stock.execute(sql)
	# res=cur_stock.fetchall()
	# for r in res:
	# 	word3=word3+"<tr><td>"+str(r[0])+"</td><td>"+str(float(r[1]))+"</td><td>"+str(float(r[2]))+"</td><td>"+str(float(r[3]))+"</td><td>"+str(float(r[4]))+"</td><td>"+str(r[5])+"</td><td>"+str(float(r[6]))+"</td><td>"+str(r[7])+"</td></tr>"
	cur_stock.close()
	conn.close()

	word='{"avg_profit":1,"avg_profit_week":1,"success":'+word2+',"success_profit":'+word4+',"max_margin":0.23,"max_huiche":0.25,"avg_num":'+word1+',"table1":"'+word3+'"'
	create_json(word)
def  create_json(word):
	file_object = open(PWD+'/json/static.json','w')
	file_object.write(word)
	file_object.close()
def  write_json(word):
	file_object = open(PWD+'/json/static.json','a')
	file_object.write(word)
	file_object.close()
def  close_json():
	file_object = open(PWD+'/json/static.json','a')
	file_object.write("}")
	file_object.close()
if __name__ == "__main__":
	global PWD
	file=open("config.ini","r")
	PWD=file.read()
	file.close()
	print(PWD)
	while(1):
		clac_json()
		getInfo("python.exe") 
		close_json()
		time.sleep(100)