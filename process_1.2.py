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
def checktick():
	filename=PWD+'/tick.csv'
	reader =os.path.getsize(filename)
	writelog("tick函数运行情况："+str(reader))

def loadcsv_add():
	open_=[]
	close=[]
	name_=[]
	date_=[]
	time_=[]
	filename=PWD+'/price_record.csv'
	sql=""
	try:
		filenode=open(filename)
	except Exception as e:
		print("Exception 了")
		try:
			time.sleep(10)
			filenode=open(filename)
		except Exception as e:
			time.sleep(10)
			filenode=open(filename)
	reader = csv.reader(filenode)
	for row in reader:
		name_.append(row[0])
		date_.append(row[1][0:10])
		time_.append(row[1][11:16])
		open_.append(row[2])
		close.append(row[3])
	filenode.close()
	#决策函数
	decision(name_,close,0.88,0.0006)
	print(len(date_))
	for i in range(len(date_)):
				
		sql=sql+"insert into stock values ('"+name_[i]+"','"+date_[i]+"','"+time_[i]+"','"+open_[i]+"',0,0,'"+close[i]+"',0,0,null);"
	cur_stock.execute(sql)
	cur_stock.close()

def loadcsv_add_clear():
	# filename='C:/Users/Administrator/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/tick.csv'
	# file_object = open(filename,'w')
	# file_object.write("")
	# file_object.close()
	filename=PWD+'/price_record.csv'
	os.remove(filename)

def releation_mid(sample,tablename):#计算个股与指标之间的相关度
	close_1=[]
	close_2=[]
	date1=[]
	stockid=[]
	time1=[]
	lnA_B=[]
	lnA_B_sub=[]
	a=[]
	b=[]
	#sql="SELECT stockid FROM stock_foreign.stock GROUP BY stockid;"
	sql="SELECT stockid FROM stock  GROUP BY stockid;"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	print(str(tablename)+"函数内取出的值",len(res))
	if len(res)>0:
		dict1={}
		sql="INSERT INTO `releation_mid_record` SELECT SYSDATE(), stockid,sample,close_now,avgA_B,stdA_B,norm_ln_prev,norm_ln_prev2,avg_cha,std_cha,norm_cha_prev, norm_cha_prev2 FROM `releation_mid`; "
		cur_result.execute(sql)
		sql="DELETE FROM `releation_mid`;"
		cur_result.execute(sql)
		for r in res:
			stockid.append(r[0])

		for i in range(len(stockid)):
		
			sql=" SELECT DISTINCT a.date,a.time,a.close FROM stock a   WHERE a.stockid= '"+stockid[i]+ "'  ORDER BY  STR_TO_DATE(CONCAT(a.date,' ',a.TIME),'%Y.%c.%d %H:%i') DESC LIMIT "+str(sample+3)
			#print(sql)
			cur_stock.execute(sql)
			res=cur_stock.fetchall()
			for r in res:
				try:
					close_1.append(float(r[2]))
					date1.append(str(r[0]))
					time1.append(str(r[1]))
					#print(float(r[2]))
				except Exception as e:
					print(str(r[1]),str(r[0]),"C端读入数据有问题")
			for r in range(0,len(close_1)):
				if r>0:

					lnA_B_sub.append(round(close_1[r-1]-close_1[r],6))
					
				
			#print(lnA_B_sub[0:sample])
			#print(len(close_1))
			if len(close_1)>=sample:
				#print(sum(close_1[2:close_1+2]))
				sql="insert into "+str(tablename)+" values('"+stockid[i]+"','"+str(sample)+"','"+str(close_1[0])+"','"+str(sum(close_1[0:sample])/len(close_1[0:sample]))+"','"+str(stdev(close_1[0:sample]))+"','"+str(scipy.stats.norm.cdf(close_1[0],sum(close_1[1:sample+1])/len(close_1[1:sample+1]),stdev(close_1[1:sample+1])))+"','"+str(scipy.stats.norm.cdf(close_1[1],sum(close_1[2:sample+2])/len(close_1[2:sample+2]),stdev(close_1[2:sample+2])))+"','"+str(sum(lnA_B_sub[0:sample])/len(lnA_B_sub[0:sample]))+"','"+str(stdev(lnA_B_sub[0:sample]))+"','"+str(scipy.stats.norm.cdf(lnA_B_sub[0],sum(lnA_B_sub[1:sample+1])/len(lnA_B_sub[1:sample+1]),stdev(lnA_B_sub[1:sample+1])))+"','"+str(scipy.stats.norm.cdf(lnA_B_sub[1],sum(lnA_B_sub[2:sample+2])/len(lnA_B_sub[2:sample+2]),stdev(lnA_B_sub[2:sample+2])))+"');"
				cur_result.execute(sql)
			else:
				print(stockid[i],"并不够"+str(sample)+"条记录")
			# print(str(pearson(close_1,close_2)))
			# print(str(pearson(per_1,per_2)))
			# print(str(pearson(close_1[0:30],close_2[0:30])))
			# print(str(pearson(per_1[0:30],per_2[0:30])))
			# print(str(pearson(close_1[0:500],close_2[0:500])))
			# print(str(pearson(per_1[0:500],per_2[0:500])))
			# print(len(res))

			close_1=[]
			close_2=[]
			lnA_B=[]
			date1=[]
			time1=[]
			lnA_B_sub=[]
def pearson(x,y):
	stockid=[]
	time1=[]
	n=len(x)
	vals=range(n)
	# Simple sums
	sumx=sum([float(x[i]) for i in vals])
	sumy=sum([float(y[i]) for i in vals])
	# Sum up the squares

	sumxSq=sum([x[i]**2.0 for i in vals])
	sumySq=sum([y[i]**2.0 for i in vals])
	# Sum up the products
	pSum=sum([x[i]*y[i] for i in vals])
	# Calculate Pearson score
	num=pSum-(sumx*sumy/n)
	den=((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)/n))**.5
	if den==0: return 0
	r=num/den
	return r



def st_norm(u):
	x=abs(u)/math.sqrt(2)
	T=(0.0705230784,0.0422820123,0.0092705272,0.0001520143,0.0002765672,0.0000430638)
	E=1-pow((1+sum([a*pow(x,(i+1)) for i,a in enumerate(T)])),-16)
	p=0.5-0.5*E if u<0 else 0.5+0.5*E
	return(p)
  
def norm(x,a,sigma):

	u=(x-a)/sigma
	return(st_norm(u))

def stdev(self):
	if len(self) < 1:
		return None
	else:
		avg = sum(self)/len(self)
		sdsq = sum([(i - avg) ** 2 for i in self])
		stdev = (sdsq / (len(self) - 1)) ** .5
		return stdev





def write_API(stockid,lnA_B_now,lnA_B_except,orderid,bucang):
	file_object = open(PWD+"/create.txt",'w')
	json=""
	writelog("有订单生成，订单数"+str(len(stockid)))
	for r in range(len(stockid)):
		json=json+str(stockid[r])+","+str(round(lnA_B_now[r],5))+","+str(round(lnA_B_except[r],5))+","+str(orderid[r])+","+str(bucang[r])+","+str(orderid[r][0:3])+"\n"

	print("有订单生成",orderid,stockid)
	file_object.write(json)
	file_object.close()

#def clac_except():
def result_DB(stockid,lnA_B_now,lnA_B_except,norm_now,norm_cha,orderid,bucang):
	sql=""
	for r in range(len(stockid)):
		sql=sql+"insert into `order` values ('"+str(orderid[r])+"','"+str(stockid[r])+"','"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"','"+str(round(lnA_B_now[r],5))+"','"+str(round(lnA_B_except[r],5))+"','"+str(norm_now[r])+"','"+str(norm_cha[r])+"','"+str(bucang[r])+"');"
	cur_result_DB.execute(sql)
	cur_result_DB.close()

def update_M_flag(stockid,flag):
	sql=""
	for r in range(len(stockid)):
		sql=sql+"update model_config set flag='"+str(flag[r])+"' where stockid='"+str(stockid[r])+"';"
	cur_update_stock.execute(sql)
	cur_update_stock.close()
def decision(name,close,norm_list,commission):
	bucang=[]
	stockA=[]
	stockB=[]
	releation=[]
	lnA_B=[]
	avgA_B=[]
	stdA_B=[]
	lnA_B_now=[]
	norm_now=[]
	orderid=[]
	lnA_B_except=[]
	norm_cha=[]
	update_flag=[]
	update_stockid=[]
	n=len(name)
	n2=len(close)
	if n!=n2:
		print("文件读入的数据中结构不正确,name和close不匹配")
	else:

		sql="SELECT a.stockid,a.close_now,a.avgA_B,a.stdA_B,a.norm_ln_prev,a.norm_ln_prev2,a.avg_cha,a.std_cha,a.norm_cha_prev,a.norm_cha_prev2,b.flag,b.bucang_max FROM `releation_mid` a ,model_config b where a.stockid=b.stockid and b.open_status=1"
		cur_d.execute(sql)
		res=cur_d.fetchall()
		print("decision",len(res))
		if len(res)>0:
			for r in res:
				if scipy.stats.norm.cdf(float(close[name.index(str(r[0]))])-float(r[1]),float(r[6]),float(r[7]))+float(r[8])+float(r[9])>0.9*3 or  scipy.stats.norm.cdf(float(close[name.index(str(r[0]))])-float(r[1]),float(r[6]),float(r[7]))+float(r[8])+float(r[9])<0.1*3 :
					update_flag.append(0)
					update_stockid.append(str(r[0]))
				else:
					update_flag.append(int(r[10])+1)
					update_stockid.append(str(r[0]))
				#print(float(close[name.index(str(r[0]))]))
				#print(scipy.stats.norm.cdf(float(close[name.index(str(r[0]))]),float(r[2]),float(r[3])))
				#print(scipy.stats.norm.cdf(float(close[name.index(str(r[0]))])-float(r[1]),float(r[6]),float(r[7])))
				#print(float(r[4]))
				#print(float(r[5]))
				#print(int(r[10]))
				if  scipy.stats.norm.cdf(float(close[name.index(str(r[0]))]),float(r[2]),float(r[3]))>norm_list and scipy.stats.norm.cdf(float(close[name.index(str(r[0]))]),float(r[2]),float(r[3]))<0.99  and scipy.stats.norm.cdf(float(close[name.index(str(r[0]))])-float(r[1]),float(r[6]),float(r[7]))<0.9 and float(r[4])<0.88 and float(r[5])<0.88 and int(r[10])>100 :
					#print(abs(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5]))-scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5]))))
					#print(float(r[3]))
					#print(scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5])))
					#print(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5])))
					stockA.append(str(r[0]))
					lnA_B.append(float(r[1]))
					avgA_B.append(float(r[2]))
					stdA_B.append(float(r[3]))
					lnA_B_now.append(float(close[name.index(str(r[0]))]))
					norm_now.append(scipy.stats.norm.cdf(float(close[name.index(str(r[0]))]),float(r[2]),float(r[3])))
					lnA_B_except.append(scipy.stats.norm.ppf(norm_list-0.03,float(r[2]),float(r[3])))
					orderid.append("0.9_"+str(time.time()+random.random()))
					norm_cha.append(scipy.stats.norm.cdf(float(close[name.index(str(r[0]))])-float(r[1]),float(r[6]),float(r[7])))
					if  float(close[name.index(str(r[0]))])/125<=float(r[11]):
						bucang.append(float(r[11]))
					else:
						bucang.append(round(float(close[name.index(str(r[0]))])/125,3))
				if  scipy.stats.norm.cdf(float(close[name.index(str(r[0]))]),float(r[2]),float(r[3]))<(1-norm_list) and scipy.stats.norm.cdf(float(close[name.index(str(r[0]))]),float(r[2]),float(r[3]))>0.01 and scipy.stats.norm.cdf(float(close[name.index(str(r[0]))])-float(r[1]),float(r[6]),float(r[7]))>0.1 and float(r[4])>0.12 and float(r[5])>0.12 and int(r[10])>100:
					#print(abs(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5]))-scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5])))):
					#print(abs(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5]))-scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5]))))
					#print(float(r[3]))
					#print(scipy.stats.norm.cdf(float(r[3]),float(r[4]),float(r[5])))
					#print(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5])))
					stockA.append(str(r[0]))
					lnA_B.append(float(r[1]))
					avgA_B.append(float(r[2]))
					stdA_B.append(float(r[3]))
					lnA_B_now.append(float(close[name.index(str(r[0]))]))
					norm_now.append(scipy.stats.norm.cdf(float(close[name.index(str(r[0]))]),float(r[2]),float(r[3])))
					lnA_B_except.append(scipy.stats.norm.ppf((1-norm_list+0.03),float(r[2]),float(r[3]))*(1+commission))
					norm_cha.append(scipy.stats.norm.cdf(float(close[name.index(str(r[0]))])-float(r[1]),float(r[6]),float(r[7])))
					orderid.append("0.1_"+str(time.time()+random.random()))
					if  float(close[name.index(str(r[0]))])/125<=float(r[11]):
						bucang.append(float(r[11]))
					else:
						bucang.append(round(float(close[name.index(str(r[0]))])/125,3))
			#print(norm_now)
		#如果releation>0.9 且 norm>0.99 就可以满足下单
			if len(stockA)>0:
				write_API(stockA,lnA_B_now,lnA_B_except,orderid,bucang)
				result_DB(stockA,lnA_B_now,lnA_B_except,norm_now,norm_cha,orderid,bucang)
			if len(update_stockid)>0:
				update_M_flag(update_stockid,update_flag)
def writelog(str):
	file=open("mail.ini","a")
	file.write(str+"\n")
	file.close()
def checkDB():

	return "程序运行稳定" 

		#if len(res)>0:
			#for r in res:
				#writelog("总共相关计算数："+str(r[0])+",最大相关数:"+str(r[1]))
									
if __name__ == "__main__":
	global PWD
	file=open("config.ini","r")
	PWD=file.read()
	file.close()
	print(PWD)
	while(1):
		if (os.path.exists(PWD+"/price_record.csv")!=0):
			conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
			cur_stock=conn.cursor()
			cur_result=conn.cursor()
			cur_d=conn.cursor()
			cur_check=conn.cursor()
			cur_stock_releation=conn.cursor()
			cur_result_DB=conn.cursor()
			cur_update_stock=conn.cursor()
			#time.sleep(2)
			loadcsv_add()
			print("step0 有文件生成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			checktick()
			time1=time.time()
			
			cur_result_DB.close()
			cur_update_stock.close()
			cur_result.close()
			cur_d.close()
			cur_check.close()
			cur_stock_releation.close()
			conn.commit()
			conn.close()
			print("step1 loadcsv_add完成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			time2=time.time()
			conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
			cur_stock=conn.cursor()
			cur_result=conn.cursor()
			cur_d=conn.cursor()
			cur_check=conn.cursor()
			cur_result_DB=conn.cursor()
			cur_stock_releation=conn.cursor()
			cur_update_stock=conn.cursor()
			releation_mid(100,"releation_mid")
			print("step2 releation_mid完成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			writelog("计算相关性用时"+str(time.time()-time2))
			time.sleep(100)
			#print(scipy.stats.norm.cdf(3,1,2))
			loadcsv_add_clear()
			print("step3 loadcsv_add_clear完成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			writelog("整体用时"+str(time.time()-time1))

			#mail.run("mail.ini",checkDB()+",我自己的测试结果测试结果,当前时间的")
			cur_stock.close()
			cur_update_stock.close()
			cur_result.close()
			cur_d.close()
			cur_check.close()
			cur_result_DB.close()
			cur_stock_releation.close()
			conn.commit()
			conn.close()

	# conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# cur_stock=conn.cursor()
	# cur_result=conn.cursor()
	# cur_d=conn.cursor()
	# cur_check=conn.cursor()
	# cur_result_DB=conn.cursor()
	# cur_stock_releation=conn.cursor()
	# releation_mid(100,"releation_mid")
	# cur_result.close()
	# cur_d.close()
	# cur_check.close()
	# cur_result_DB.close()
	# cur_stock_releation.close()
	# conn.commit()
	# conn.close()