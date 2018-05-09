import os
from collections import defaultdict
import random
import csv
cmd = 'aws s3 cp s3://zhousq12cw/mt.csv /home/ec2-user/mt.csv'
cmd2 = 'aws s3 cp /home/ec2-user/mt.csv s3://zhousq12cw/mt.csv'
cmd3 = 'aws s3 cp s3://zhousq12cw/value.csv /home/ec2-user/value.csv'
os.system("aws configure set aws_access_key_id XXX(YOURS ACCESS KEY)")
os.system("aws configure set aws_secret_access_key XXX(YOURS SECRT KEY)")
os.system("aws configure set default.region eu-west-2")
os.system(cmd)
os.system(cmd3)
list95 = []
list99 = []
returnlist = []
columns = defaultdict(list)
with open('/home/ec2-user/value.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k,v) in row.items():
                columns[k].append(v)
p = columns['p']
p = float(''.join(p))
mean = columns['mean']
mean = float(''.join(mean))
dev = columns['deviation']
dev = float(''.join(dev))
Z = columns['Z']
Z = ''.join(Z)
Y = int(Z)

a = [random.gauss(mean,dev) for i in range(Y)]
b = [ (i + 1) * p for i in a ]
for i in range(len(b)-1):
	returnlist.append((float(b[i])-float(b[i+1]))/float(b[i+1]))
sortlist = sorted(returnlist, reverse=True)
n95 = int(round(len(sortlist)* 0.95)-1)
n99 = int(round(len(sortlist)* 0.99)-1)
list95.append(sortlist[n95])
list99.append(sortlist[n99])
mean95 = sum(list95)/float(len(list95))
mean99 = sum(list99)/float(len(list99))
#!!!!!!!!!!!!!
with open('/home/ec2-user/mt.csv''a') as f:
	f.write('\r\n');
	writer = csv.writer(f)
	writer.writerow([mean95, mean99])

os.system(cmd2)
