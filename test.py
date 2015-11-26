#coding:utf-8
import threading
import urllib
import urllib.request
import csv
import pymysql
import time
import math
from datetime import timedelta, date
import linecache

def loadcsv_add():
	open_=[]
	close=[]
	name_=[]
	date_=[]
	time_=[]
	filename='C:/Users/liuhao_yy/AppData/Roaming/MetaQuotes/Terminal/50CA3DFB510CC5A8F28B48D1BF2A5702/MQL4/Files/price_record_test.csv'
	sql=""
	reader = csv.reader(open(filename))
	for row in reader:
		name_.append(row[0])
		date_.append(row[1][0:10])
		time_.append(row[1][11:16])
		open_.append(row[2])
		close.append(row[3])
	#决策函数
	decision(name_,close,0.99,0.002)
	
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

def releation_mid(sample):#计算个股与指标之间的相关度
	close_1=[]
	close_2=[]
	date1=[]
	stockid=[]
	time1=[]
	lnA_B=[]
	close_1_Sq=[]
	close_2_Sq=[]
	close12=[]
	a=[]
	b=[]
	sql="SELECT stockid FROM stock_foreign.stock GROUP BY stockid;"
	cur_stock.execute(sql)
	res=cur_stock.fetchall()
	print("releation_mid函数内取出的值",len(res))
	if len(res)>1:
		dict1={}
		sql="delete from releation_mid_test;"
		cur_result.execute(sql)
		for r in res:
			stockid.append(r[0])
		for i in range(len(stockid)):
			for j in range(len(stockid)):
				if i<j:

					sql="select DISTINCT a.date,a.time,a.close,b.close from stock a ,stock b where a.stockid='"+stockid[i]+"' and b.stockid='"+stockid[j]+"' and a.date=b.date and a.time=b.time ORDER BY  STR_TO_DATE(CONCAT(a.date,' ',a.TIME),'%Y.%c.%d %H:%i') desc LIMIT "+str(sample)
					cur_stock.execute(sql)
					res=cur_stock.fetchall()
					for r in res:
						try:
							lnA_B.append(math.log(float(r[2])) - math.log(float(r[3])))
							close_1.append(float(r[2]))
							close_2.append(float(r[3]))
							date1.append(str(r[0]))
							time1.append(str(r[1]))
							close_1_Sq.append(float(r[2])**2.0)
							close_2_Sq.append(float(r[3])**2.0)
							close12.append(float(r[2])*float(r[3]))
						except Exception as e:
							print(str(r[1]),str(r[0]),"C端读入数据有问题")
					#print(time1[0])
					
					if len(close_1)>=sample:

						sql="insert into releation_mid_test values('"+stockid[i]+"','"+stockid[j]+"','"+str(sample)+"','"+str(pearson(close_1,close_2))+"','"+str(lnA_B[len(lnA_B)-1])+"','"+str(sum(lnA_B)/len(lnA_B))+"','"+str(stdev(lnA_B))+"','"+str(float(sum(close12[0:len(close12)-1])))+"','"+str(float(sum(close_1[0:len(close_1)-1])))+"','"+str(float(sum(close_2[0:len(close_2)-1])))+"','"+str(float(sum(close_1_Sq[0:len(close_1_Sq)-1])))+"','"+str(float(sum(close_2_Sq[0:len(close_2_Sq)-1])))+"');"
						cur_result.execute(sql)
					else:
						print(stockid[i],stockid[j],"并不够"+str(sample)+"条记录")


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
	print(sumx)
	sumy=sum([float(y[i]) for i in vals])
	# Sum up the squares
	print(sumy)
	sumxSq=sum([x[i]**2.0 for i in vals])
	sumySq=sum([y[i]**2.0 for i in vals])
	print(sumxSq)
	print(sumySq)
	pSum=sum([x[i]*y[i] for i in vals])
	# Calculate Pearson score
	print(pSum)
	num=pSum-(sumx*sumy/n)
	den=((sumxSq-pow(sumx,2)/n)*(sumySq-pow(sumy,2)/n))**.5
	if den==0: return 0
	r=num/den
	return r
def pearson2(n,x,y,psum99,sumx99,sumy99,sumxSq99,sumySq99):
	num=psum99+x*y-(sumx99+x)*(sumy99+y)/n
	den=((sumxSq99+x**2-(sumx99+x)**2/n)*(sumySq99+y**2-(sumy99+y)**2/n))**.5
	if den==0: return 0
	r=num/den
	return r

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
		
		sql="SELECT stockidA, stockidB ,releation ,lnA_B,avgA_B,stdA_B,pSum_99,sumx99,sumy99,sumxSq99,sumySq99 FROM releation_mid_test;"
		cur_d.execute(sql)
		res=cur_d.fetchall()
		print("decision",len(res))
		if len(res)>0:
			for r in res:
				print(str(r[0]),str(r[1]),str(pearson2(100,float(close[name.index(str(r[0]))]),float(close[name.index(str(r[1]))]),float(r[6]),float(r[7]),float(r[8]),float(r[9]),float(r[10]))))
				# if float(r[2])>0.9 and pearson2(100,float(close[name.index(str(r[0]))]),float(close[name.index(str(r[1]))]),float(r[6]),float(r[7]),float(r[8]),float(r[9]),float(r[10]))<0.9 and scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])+commission),float(r[4]),float(r[5]))>norm_list:#获取每一组A和B在参数的位置，并找出位置的close为现价，做计算后合并为lnA_B_now
				# 	stockA.append(str(r[0]))
				# 	stockB.append(str(r[1]))
				# 	releation.append(float(r[2]))
				# 	lnA_B.append(float(r[3]))
				# 	avgA_B.append(float(r[4]))
				# 	stdA_B.append(float(r[5]))
				# 	lnA_B_now.append(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])))
				# 	normA_B_now.append(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])+commission),float(r[4]),float(r[5])))
				# 	lnA_B_except.append(scipy.stats.norm.ppf(norm_list,float(r[4]),float(r[5])))
				# 	orderid.append("0.9_0.99_"+str(time.time()+random.random()))
				# if float(r[2])>0.9 and pearson2(100,float(close[name.index(str(r[0]))]),float(close[name.index(str(r[1]))]),float(r[6]),float(r[7]),float(r[8]),float(r[9]),float(r[10]))<0.9 and scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])-commission),float(r[4]),float(r[5]))<(1-norm_list):#获取每一组A和B在参数的位置，并找出位置的close为现价，做计算后合并为lnA_B_now
				# 	stockA.append(str(r[1]))
				# 	stockB.append(str(r[0]))
				# 	releation.append(float(r[2]))
				# 	lnA_B.append(float(r[3]))
				# 	avgA_B.append(float(r[4]))
				# 	stdA_B.append(float(r[5]))
				# 	lnA_B_now.append(-math.log(float(close[name.index(str(r[0]))]))+math.log(float(close[name.index(str(r[1]))])))
				# 	normA_B_now.append(scipy.stats.norm.cdf(math.log(float(close[name.index(str(r[0]))]))-math.log(float(close[name.index(str(r[1]))])-commission),float(r[4]),float(r[5])))
				# 	lnA_B_except.append(-scipy.stats.norm.ppf((1-norm_list),float(r[4]),float(r[5])))
				# 	orderid.append("0.9_0.01_"+str(time.time()+random.random()))
			#print(normA_B_now)
		#如果releation>0.9 且 norm>0.99 就可以满足下单

def write_result(a,b):
	file_object = open('result.csv','w')
	for i in range(len(a)):
		file_object.write(str(a[i])+","+str(b[i])+"\n")
	file_object.close()

if __name__ == '__main__':

		write_result([1,100],[2,200])