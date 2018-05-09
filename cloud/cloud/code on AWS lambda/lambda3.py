import boto3
import os
import csv
import time

os.system("aws configure set aws_access_key_id XXXX(you access key)")
os.system("aws configure set aws_secret_access_key XXXX(you secret key)")
os.system("aws configure set default.region eu-west-2")
shell = """#!/bin/bash
sudo python /home/ec2-user/1.py
"""
shell2 = """#!/bin/bash
sudo python /home/ec2-user/2.py
"""

def lambda_handler(event, context):
    M = int(event['M'])
    R = int(event['R'])
    deviation = float(event['dev'])
    mean = float(event['mean'])
    p= float(event['p'])

    #now = str(event['now'])

    Z = M//R
    Y = M//R+M%R
    with open('/tmp/value.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(('p','mean','deviation','Z','Y'))
        writer.writerow((p,mean,deviation,Z,Y))
  
    with open('/tmp/mt.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(['95%','99%'])
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('/tmp/value.csv', 'zhousq12cw', 'value.csv')
    s3.meta.client.upload_file('/tmp/mt.csv', 'zhousq12cw', 'mt.csv')
    os.system("rm -f /tmp/value.csv")
    #os.system("rm -f '/tmp/mt_%s.csv %now'")
    #run instance
    client = boto3.client('ec2')
    if R == 1:
        response2 = client.run_instances(ImageId='ami-fdabbf99', MinCount=1, MaxCount=1,InstanceType='t2.micro', UserData=shell2,KeyName='mac-euwestkp')
    else:
        response = client.run_instances(ImageId='ami-fdabbf99', MinCount=1, MaxCount=(int(R)-1),InstanceType='t2.micro', UserData=shell,KeyName='mac-euwestkp')
        time.sleep(5)
        response2 = client.run_instances(ImageId='ami-fdabbf99', MinCount=1, MaxCount=1,InstanceType='t2.micro', UserData=shell2,KeyName='mac-euwestkp')

    
    