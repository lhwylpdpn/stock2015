
import random
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



def function2(a):
	t=[]
	t.append(100)
	g=0
	for i in range(1,1440):

		t.append(t[i-1]+random.random()-random.random())
		if t[i-1]<100-a:
			g=g+1
	return g/1440

		

if __name__ == '__main__':
	file=open("test/result.csv","w")

	for j in range(1,40):
		m=[]
		for i in range(1,10000):
			s=function2(j/4)

			if s is not None:
				m.append(s)

			
		print(sum(m)/len(m),clac1(sum(m)/len(m),0.93,j/4))
		file.write(str(sum(m)/len(m))+",0.93,"+str(j/2)+","+str(clac1(sum(m)/len(m),0.96,j/4))+"\n")

	file.close()