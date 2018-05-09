import datetime
import random
returnlist = []
list95 = []
list99 = []
def time_1():
	begin = datetime.datetime.now()
	a = [random.gauss(1,1) for i in range(2000000)]
	b = [ (i + 1) * 10 for i in a ]
	for i in range(len(b)-1):
		returnlist.append((float(b[i])-float(b[i+1]))/float(b[i+1]))
	sortlist = sorted(returnlist, reverse=True)
	n95 = int(round(len(sortlist)* 0.95)-1)
	n99 = int(round(len(sortlist)* 0.99)-1)
	list95.append(sortlist[n95])
	list99.append(sortlist[n99])
	mean95 = sum(list95)/float(len(list95))
	mean99 = sum(list99)/float(len(list99))
	end = datetime.datetime.now()
	return end-begin
	
print time_1()
