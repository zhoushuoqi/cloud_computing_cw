import boto3
import os
import csv
import time

os.system("aws configure set aws_access_key_id XXX(yours access key)")
os.system("aws configure set aws_secret_access_key XXXX(yours secret key)")
os.system("aws configure set default.region eu-west-2")
def lambda_handler(event, context):
    I = float(event['investment'])
    time.sleep(23)
    s3 = boto3.resource('s3')
    s3.meta.client.download_file('zhousq12cw', 'result.csv', '/tmp/result.csv')
    
    with open('/tmp/result.csv') as f:
	rows = csv.reader(f)
	for row in rows:
		VaR5 = row[0] 
		VaR6 = row[1] 
		VaR5 = float(VaR5)* I
		VaR6 = float(VaR6)* I
	result = [VaR5,VaR6]
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    ids = []
    for instance in instances:
    	ids.append(instance.id)
    ec2.instances.filter(InstanceIds=ids).terminate()
    return result