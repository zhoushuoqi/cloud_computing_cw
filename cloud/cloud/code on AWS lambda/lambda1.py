import math
import ast
import boto3
import os
import csv
from collections import defaultdict
from math import sqrt
from datetime import datetime

os.system("aws configure set aws_access_key_id XXXXXX(yours access key)")
os.system("aws configure set aws_secret_access_key XXXXXX(yours secret key)")
os.system("aws configure set default.region eu-west-2")
s3 = boto3.resource('s3')
s3.meta.client.download_file('zhousq12cw', 'amazon.csv', '/tmp/amazon.csv')
s3.meta.client.download_file('zhousq12cw', 'apple.csv', '/tmp/apple.csv')
s3.meta.client.download_file('zhousq12cw', 'google.csv', '/tmp/google.csv')
s3.meta.client.download_file('zhousq12cw', 'ibm.csv', '/tmp/ibm.csv')
s3.meta.client.download_file('zhousq12cw', 'oracle.csv', '/tmp/oracle.csv')

def lambda_handler(event, context):
    I = float(event['investment'])
    M = int(event['M'])
    R = int(event['R'])
    T = int(event['T'])
    name = str(event['name'])


    #############
    
    if name == 'amazon':
        path = '/tmp/amazon.csv'
    elif name =='apple':
        path = '/tmp/apple.csv'
    elif name =='google':
        path = '/tmp/google.csv'
    elif name =='ibm':
        path = '/tmp/ibm.csv'
    elif name =='oracle':
        path = '/tmp/oracle.csv'
    elif name =='other':
        path = '/tmp/other.csv'
    #Historical
    columns = defaultdict(list) 
    with open(path) as f:
        reader = csv.DictReader(f) 
        for row in reader: 
            for (k,v) in row.items(): 
                columns[k].append(v)
    returnlist_his = []   
    Adj = columns['Adj Close']
    p = Adj[0]
    for i in range(len(Adj)-1):
        returnlist_his.append((float(Adj[i])-float(Adj[i+1]))/float(Adj[i+1]))
    returnlist_his2 = returnlist_his[:(T)]
    sortlreturnlist_his2 = sorted(returnlist_his2, reverse=True)
    VaR1 = sortlreturnlist_his2[int(round(len(sortlreturnlist_his2)* 0.95)-1)]*I
    VaR2 = sortlreturnlist_his2[int(round(len(sortlreturnlist_his2)* 0.99)-1)]*I
    #Covariance
    mean = sum(returnlist_his2)/float(len(returnlist_his2))
    differences = [x - mean for x in returnlist_his2]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd / (len(returnlist_his2)-1)
    deviation = sqrt(variance)
    VaR3 = - (mean + (1.65 * deviation)) * I
    VaR4 = - (mean + (2.33 * deviation)) * I
    #format return serial
    l = []
    for i,each in enumerate(returnlist_his2,start=1):
		l.append(["{}, {}".format(i,each)])
    lst = str(l).translate(None, "'")
    
    #format time serial
    a = [float(x) for x in columns['Adj Close']]
    a2 = a[:T]
    b = [str(x) for x in columns['Date']]
    b2 = b[:T]
    data = [VaR1,VaR2,VaR3,VaR4,mean,deviation,p,lst,a2,b2]
    return data