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
	filename='C:/Users/liuhao_yy/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/tick.csv'
	reader =os.path.getsize(filename)
	writelog("tick函数运行情况："+str(reader))

def loadcsv_add():
	open_=[]
	close=[]
	name_=[]
	date_=[]
	time_=[]
	filename='C:/Users/liuhao_yy/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/price_record.csv'
	sql=""
	reader = csv.reader(open(filename))
	for row in reader:
		name_.append(row[0])
		date_.append(row[1][0:10])
		time_.append(row[1][11:16])
		open_.append(row[2])
		close.append(row[3])
	#决策函数
	decision(name_,close,0.99,0.001)
	for i in range(len(date_)):
				
		sql=sql+"insert into stock_foreign.stock values ('"+name_[i]+"','"+date_[i]+"','"+time_[i]+"','"+open_[i]+"',0,0,'"+close[i]+"',0,0,null);"
	#print(sql)
	cur_stock.execute(sql)

def loadcsv_add_clear():

	filename='C:/Users/liuhao_yy/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/price_record.csv'
	file_object = open(filename,'w')
	file_object.write("")
	file_object.close()
	filename='C:/Users/liuhao_yy/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/tick.csv'
	file_object = open(filename,'w')
	file_object.write("")
	file_object.close()
def releation_mid(sample):#计算个股与指标之间的相关度
	close_1=[]
	close_2=[]
	date1=[]
	stockid=[]
	time1=[]
	lnA_B=[]
	a=[]
	b=[]
	sql="truncate table releation_mid;"
	cur_stock.execute(sql)
	sql="select stockid from stock_foreign.stock group by stockid;"
	cur_action.execute(sql)
	res=cur_action.fetchall()
	print(len(res))
	if len(res)>1:
		dict1={}
		for r in res:
			stockid.append(r[0])
		for i in range(len(stockid)):
			for j in range(len(stockid)):
				if i<j:

					sql="select DISTINCT a.date,a.time,a.close,b.close from stock a ,stock b where a.stockid='"+stockid[i]+"' and b.stockid='"+stockid[j]+"' and a.date=b.date and a.time=b.time ORDER BY  STR_TO_DATE(CONCAT(a.date,' ',a.TIME),'%Y.%c.%d %H:%i') desc LIMIT "+str(sample)
					cur_result.execute(sql)
					res=cur_result.fetchall()

					for r in res:
						try:
							lnA_B.append(math.log(float(r[2])) - math.log(float(r[3])))
							close_1.append(float(r[2]))
							close_2.append(float(r[3]))
							date1.append(str(r[0]))
							time1.append(str(r[1]))
							#print(float(r[2]),float(r[3]),str(r[0]),str(r[1]))
							#print(math.log(float(r[2])))
							#print(math.log(float(r[3])))
						except Exception(e):
							print(str(r[1]),str(r[0]),"C端读入数据有问题")
					if len(close_1)>=sample:
					#print(pearson(close_1,close_2),close_1,close_2)
					#print(close_1[len(close_1)-1],close_2[len(close_2)-1])
						sql="insert into releation_mid values('"+stockid[i]+"','"+stockid[j]+"','"+str(sample)+"','"+str(pearson(close_1,close_2))+"','"+str(lnA_B[len(lnA_B)-1])+"','"+str(sum(lnA_B)/len(lnA_B))+"','"+str(stdev(lnA_B))+"');"
						cur_result.execute(sql)
					else:
						print(stockid[i],stockid[j],"并不够"+str(sample)+"条记录")
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

# def calc(ida,idb):#计算个股与指标之间的相关度
# 	adj_close_1=[]
# 	adj_close_2=[]
# 	date=[]
# 	stockidA=[]
# 	stockidB=[]
# 	logresult=[]
# 	sqlresult=""
# 	sql="select a.date,a.close,b.close from stock a,stock b where a.stockid='"+ida+"' and b.stockid='"+idb+"' and a.date=b.date and a.time=b.time ORDER BY DATE_FORMAT(CONCAT(a.date,' ',a.time),'%Y.%c.%d %H:%i') desc"
# 	#desc 确保按照时间倒序排序，最新数据在logrequest0

# 	cur_result.execute(sql)
# 	res=cur_result.fetchall()
# 	dict1={}
# 	for r in res:
# 		date.append(r[0])	
# 		stockidA.append(r[1])
# 		stockidB.append(r[2])
# 		logresult.append(math.log(r[1])-math.log(r[2]))
# 	#print(logresult[0])
# 	#print(sum(logresult)/len(logresult))
# 	#print(stdev(logresult))
# 	sqlresult=" insert into norm_data values ('"+ida+"','"+idb+"','"+str(stockidA[0])+"','"+str(stockidB[0])+"','"+str(norm(logresult[0],sum(logresult[0:100])/len(logresult[0:100]),stdev(logresult[0:100])))+"','"+str(norm(logresult[0],sum(logresult[0:500])/len(logresult[0:500]),stdev(logresult[0:500])))+"','"+str(norm(logresult[0],sum(logresult[0:1000])/len(logresult[0:1000]),stdev(logresult[0:1000])))+"','"+str(norm(logresult[0],sum(logresult)/len(logresult),stdev(logresult)))+"','"+str(sum(logresult[0:100])/len(logresult[0:100]))+"','"+str(sum(logresult[0:500])/len(logresult[0:500]))+"','"+str(sum(logresult[0:1000])/len(logresult[0:1000]))+"','"+str(sum(logresult)/len(logresult))+"','"+str(stdev(logresult[0:100]))+"','"+str(stdev(logresult[0:500]))+"','"+str(stdev(logresult[0:1000]))+"','"+str(stdev(logresult))+"'); "
# 	#sqlresult=" insert into norm_data values ('"+ida+"','"+idb+"',null,null,null,'"+str(norm(logresult[0],sum(logresult)/len(logresult),stdev(logresult)))+"',null,null,null,'"+str(sum(logresult)/len(logresult))+"',null,null,null,'"+str(stdev(logresult))+"'); "
# 	cur_result.execute(sqlresult)
# 	conn.commit()





# def banlace(buyprice,sellprice,except_norm,point):
# 	#假设AB都是正数
# 	#(a-buyprice+sellprice-b)/(sellprice+buyprice)=point/100
# 	b=((sellprice+buyprice)*point/100+(buyprice-sellprice))/(math.exp(except_norm)-1)
# 	a=math.exp(except_norm)*b
# 	return (a,b)
# def sign (p_gailv_high,p_gailv_low,point):#核心函数，查URL写数据库,计算指标库
# 	stocka=[]
# 	stockb=[]
# 	stocka_price=[]
# 	stockb_price=[]
# 	norm=[]
# 	norm_avg=[]
# 	norm_stdev=[]
# 	except_norm=[]
# 	except_buy_price=[]
# 	except_sell_price=[]
# 	except_buy_price_temp=""
# 	except_sell_price_temp=""
# 	sql="SELECT stockidA,stockidB,stockida_price,stockidb_price,normvalue_per_100,norm_avg_100,norm_stdev_100 FROM norm_data WHERE (normvalue_per_100> '"+str(p_gailv_high)+"' or normvalue_per_100<'"+str(p_gailv_low)+"')"
# 	cur_action.execute(sql)
# 	res=cur_action.fetchall()
# 	if len(res)>0:
# 		for r in res:
# 			norm.append(r[4])
# 			norm_avg.append(r[5])
# 			norm_stdev.append(r[6])
# 			if r[4]>p_gailv_high:
# 				stocka.append(r[1])
# 				stockb.append(r[0])
# 				stocka_price.append(r[3])
# 				stockb_price.append(r[2])
# 				except_buy_price_temp,except_sell_price_temp=banlace(r[3],r[2],-scipy.stats.norm.ppf(p_gailv_high,r[5],r[6]),point)
# 				except_buy_price.append(except_buy_price_temp)
# 				except_sell_price.append(except_sell_price_temp)
# 			if r[4]<p_gailv_low:
# 				stocka.append(r[0])
# 				stockb.append(r[1])
# 				stocka_price.append(r[2])
# 				stockb_price.append(r[3])
# 				except_buy_price_temp,except_sell_price_temp=banlace(r[2],r[3],scipy.stats.norm.ppf(p_gailv_low,r[5],r[6]),point)
# 				except_buy_price.append(except_buy_price_temp)
# 				except_sell_price.append(except_sell_price_temp)
# 		write_API(stockb,stocka,stockb_price,stocka_price,except_buy_price,except_sell_price)#调整为顺势
# 		result_DB(stockb,stocka,stockb_price,stocka_price,except_buy_price,except_sell_price)#调整为顺势

# def sign_no_limit (p_gailv_high,p_gailv_low):#核心函数，查URL写数据库,计算指标库
# 	stocka=[]
# 	stockb=[]
# 	stocka_price=[]
# 	stockb_price=[]
# 	norm=[]
# 	norm_avg=[]
# 	norm_stdev=[]
# 	except_norm=[]
# 	except_buy_price=[]
# 	except_sell_price=[]
# 	except_buy_price_temp=""
# 	except_sell_price_temp=""
# 	sql="SELECT stockidA,stockidB,stockida_price,stockidb_price,normvalue_per_100,norm_avg_100,norm_stdev_100 FROM norm_data WHERE ((stockidA='AUDCHF...60.csv' AND stockidB='CADCHF...60.csv') OR (stockidA='CADCHF...60.csv' AND stockidB='AUDCHF...60.csv')) and (normvalue_per_100> '"+str(p_gailv_high)+"' or normvalue_per_100<'"+str(p_gailv_low)+"')"
# 	cur_action.execute(sql)
# 	res=cur_action.fetchall()
# 	if any(res):
# 		for r in res:
# 			norm.append(r[4])
# 			norm_avg.append(r[5])
# 			norm_stdev.append(r[6])
# 			if r[4]>p_gailv_high:
# 				stocka.append(r[1])
# 				stockb.append(r[0])
# 				stocka_price.append(r[3])
# 				stockb_price.append(r[2])
# 				except_buy_price.append(0)
# 				except_sell_price.append(0)
# 			if r[4]<p_gailv_low:
# 				stocka.append(r[0])
# 				stockb.append(r[1])
# 				stocka_price.append(r[2])
# 				stockb_price.append(r[3])
# 				except_buy_price.append(0)
# 				except_sell_price.append(0)
# 		write_API(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price)
# 		result_DB(stocka,stockb,stocka_price,stockb_price,except_buy_price,except_sell_price)


def write_API(stocka,stockb,lnA_B,lnA_B_except,orderid):
	json=""
	file_object = open("C:/Users/liuhao_yy/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/create.txt",'w')
	writelog("有订单生成，订单数"+str(len(stocka)))
	for r in range(len(stocka)):
		#json=json+"'buyID':'"+str(stocka[r])+"',buyprice':'"+str(stocka_price[r])+"','sellID':'"+str(stockb[r])+"','sellprice':'"+str(stockb_price[r])+"','except_buy_price':'"+str(except_buy_price[r])+"','except_sell_price':'"+str(except_sell_price[r])+"'"+"\n"
		json=json+str(stocka[r])+","+str(stockb[r])+","+str(lnA_B[r])+","+str(lnA_B_except[r])+","+str(orderid[r])+"\n"
		#print(math.log(stocka_price[r])-math.log(stockb_price[r])) #buy-sell>except 就平仓
		#print(except_norm[r])
		#print(math.log(stocka_price[r]/stockb_price[r]))
		#print(math.exp(except_norm[r]))
	print("有订单生成",orderid,stocka,stockb)
	file_object.write(json)
	file_object.close()

#def clac_except():
def result_DB(stocka,stockb,lnA_B,lnA_B_except,normA_B_now,releation,orderid,avg,std):
	sql=""
	for r in range(len(stocka)):
		sql=sql+"insert into `order` values ('"+str(orderid[r])+"','"+str(stocka[r])+"','"+str(stockb[r])+"','"+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+"','"+str(lnA_B[r])+"','"+str(lnA_B_except[r])+"','"+str(normA_B_now[r])+"','"+str(releation[r])+"','"+str(avg[r])+"','"+str(std[r])+"');"
	cur_result_DB.execute(sql)
	conn.commit()



def decision(name,close,norm_list,commission):
	stockA=[]
	stockB=[]
	releation=[]
	lnA_B=[]
	avgA_B=[]
	stdA_B=[]
	lnA_B_now=[]
	normA_B_now=[]
	orderid=[]
	lnA_B_except=[]
	n=len(name)
	n2=len(close)
	if n!=n2:
		print("文件读入的数据中结构不正确,name和close不匹配")
	else:
		sql="SELECT stockidA, stockidB ,releation ,lnA_B,avgA_B,stdA_B FROM releation_mid;"
		cur_d.execute(sql)
		res=cur_d.fetchall()
		if len(res)>0:
			for r in res:
				if float(r[2])>=0.9 and scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])+commission),float(r[4]),float(r[5]))>norm_list:#获取每一组A和B在参数的位置，并找出位置的close为现价，做计算后合并为lnA_B_now
					stockA.append(str(r[0]))
					stockB.append(str(r[1]))
					releation.append(float(r[2]))
					lnA_B.append(float(r[3]))
					avgA_B.append(float(r[4]))
					stdA_B.append(float(r[5]))
					lnA_B_now.append(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])))
					normA_B_now.append(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])),float(r[4]),float(r[5])))
					lnA_B_except.append(scipy.stats.norm.ppf(norm_list,float(r[4]),float(r[5])))
					orderid.append(str(time.time()+random.random()))
			#print(normA_B_now)
		#如果releation>0.9 且 norm>0.99 就可以满足下单
			if len(stockA)>0:
				write_API(stockB,stockA,lnA_B_now,lnA_B_except,orderid)
				result_DB(stockB,stockA,lnA_B_now,lnA_B_except,normA_B_now,releation,orderid,avgA_B,stdA_B)
def writelog(str):
	file=open("mail.ini","a")
	file.write(str+"\n")
	file.close()
def checkDB():
		sql="SELECT SUM(a.a-b.a+1),a.stockid FROM tempone a, (SELECT COUNT(*) AS a,stockid FROM stock GROUP BY stockid) b  WHERE a.`stockid`= b.stockid;DROP   TABLE tempone;CREATE  TABLE  tempone SELECT COUNT(*) AS a,stockid FROM stock GROUP BY stockid;"
		cur_check.execute(sql)
		res=cur_check.fetchall()
		if len(res)>0:
			for r in res:
				writelog("入库数据量差别，正常值为0："+str(r[0]))
		sql="SELECT STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') FROM stock GROUP BY STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') DESC LIMIT 2;"
		cur_check.execute(sql)

		res=cur_check.fetchall()
		if len(res)>0:
			for r in res:
				writelog("两次数据时间分别是："+str(r[0]))
		sql="SELECT COUNT(*),MAX(releation) FROM `releation_mid`;"
		cur_check.execute(sql)
		res=cur_check.fetchall()
		if len(res)>0:
			for r in res:
				writelog("总共相关计算数："+str(r[0])+",最大相关数:"+str(r[1]))
										
if __name__ == "__main__":
	#write_API("GBPUSD","USDCHF",-0.24836,-0.401,"33133333333333")
	# conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# cur_stock=conn.cursor()
	# cur_action=conn.cursor()
	# releation_mid(100)
	#loadcsv_add_clear()
	while(1):
		if (os.path.getsize("C:/Users/liuhao_yy/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/price_record.csv")!=0):
			conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
			cur_stock=conn.cursor()
			cur_action=conn.cursor()
			cur_result=conn.cursor()
			cur_d=conn.cursor()
			cur_check=conn.cursor()
			cur_result_DB=conn.cursor()
			print("step0 有文件生成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			checktick()
			time1=time.time()
			loadcsv_add()
			print("step1 loadcsv_add完成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			time2=time.time()
			releation_mid(100)
			print("step2 releation_mid完成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			writelog("计算相关性用时"+str(time.time()-time2))
			#print(scipy.stats.norm.cdf(3,1,2))
			loadcsv_add_clear()
			print("step3 loadcsv_add_clear完成"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			checkDB()
			writelog("整体用时"+str(time.time()-time1))

			mail.run()#test()
			conn.commit()
			




	#print(scipy.stats.norm.ppf(0.99,0.00468906,0.49432524))

	# while(1):

	# 	if  (os.path.getsize("C:/Users/Administrator/AppData/Roaming/MeaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/API_callback.csv")!=0):
	# 		conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='stock_foreign',port=3306)
	# 		cur_stock=conn.cursor()
	# 		cur_action=conn.cursor()
	# 		cur_result=conn.cursor()
	# 		print("有新增数据入库"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
			
	
	# 		cur_stock.execute("delete from releation")
	# 		loadcsv_add()
	# 		calc1()
	# 		cur_result.execute("delete from norm_data")
	# 		stockid=[]
	# 		sql233="SELECT stockidA,stockidB FROM `releation` WHERE   relation_per_1000>0.93 LIMIT 10"
	# 		cur_result.execute(sql233)
	# 		res=cur_result.fetchall()
	# 		for j in res:
	# 			calc(j[0],j[1])
	# 		sign(0.99,0.01,0.15)
	# 		print("计算完成step1"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
	# 		sign_no_limit(0.99,0.01)
	# 		print("计算完成step2"+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
	# 		cur_result.close()
	# 		cur_action.close()
	# 		cur_stock.close()
	# 		conn.close()
	# 		time.sleep(60)
	# 		loadcsv_add_clear()

