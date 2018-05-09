import random


def lambda_handler(event, context):
    list95 = []
    list99 = []
    returnlist = []
    Z = int(event['Z'])
    p = float(event['p'])
    mean = float(event['mean'])
    deviation = float(event['dev'])
    a = [random.gauss(mean,deviation) for i in range(Z)]
    b = [ (i + 1) * p for i in a ]
    for i in range(len(b)-1):
        returnlist.append((float(b[i])-float(b[i+1]))/float(b[i+1]))
            
    sortlist = sorted(returnlist, reverse=True)
    n95 = sortlist[int(round(len(sortlist)* 0.95)-1)]
    n99 = sortlist[int(round(len(sortlist)* 0.99)-1)]
    return n95,n99
    