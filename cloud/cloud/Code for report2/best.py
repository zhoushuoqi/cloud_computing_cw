import random
import matplotlib.pyplot as plt

list95 = []
list99 = []
returnlist = []
Z2 = []
n = []
Z = 10000
p = 827.460022
mean = 0.001983
deviation = 0.039541
for i in range(50):
    Z+=10000
    Z2.append(Z)
print Z2
for item in Z2:
    a = [random.gauss(mean,deviation) for i in range(item)]
    b = [ (i + 1) * p for i in a ]
    for i in range(len(b)-1):
        returnlist.append((float(b[i])-float(b[i+1]))/float(b[i+1]))
            
    sortlist = sorted(returnlist, reverse=True)
    n95 = sortlist[int(round(len(sortlist)* 0.95)-1)]
    n99 = sortlist[int(round(len(sortlist)* 0.99)-1)]
    n.append(n95)
print n
plt.plot(Z2,n,'ro')
plt.ylabel('some numbers')
plt.show()