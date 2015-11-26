import math
import random


def clac_zt(x,y):
	r=1
	i=1
	i_zt=0
	i_zysa=0
	i_zysb=0
	while(1):
		r=r*(1+random.random()*0.0009-random.random()*0.0009)
		i=i+1
		if r>1+x:
			i_zt=1
			break
		elif r>1+y:
			i_zysa=1
			break
		elif r<1-y:
			i_zysb=1
			break
	print(i_zt*100000000+i_zysa*1+i_zysb*0.0001)
	return(i_zt*100000000+i_zysa*1+i_zysb*0.0001)
def clac_zys_a(x):
	r=1
	i=1
	while(1):
		r=r*(1+random.random()*0.0009-random.random()*0.0009)
		i=i+1
		if r>1+x or i>10000:
			break
	return i
def clac_zys_b(x):
	r=1
	i=1
	while(1):
		r=r*(1+random.random()*0.0009-random.random()*0.0009)
		i=i+1
		if r<1-x or i>10000:
			break
	return i
if __name__ == '__main__': 
	i=1
	j=0
	j_a=0
	j_b=0
	k=0
	res=0
	while(i<100):
		i=i+1
		res=res+clac_zt(0.0025,0.1)
	print(res)