from __future__ import print_function
import requests
from dateutil import parser

import boto3
import json


request = requests.get('https://cat-fact.herokuapp.com/facts')

abcd = json.loads(request.text)
#print((abcd['all']))

    
#print(request.status_code)


def store_dynamo_db(_id, type, upvotes):

    print(upvotes,"upvotes")
    ACCESS_KEY =""
    SECRET_KEY = ""
    dynamo = boto3.resource('dynamodb',region_name='us-east-1')
    table = dynamo.Table('cat')

    from decimal import Decimal
    table.put_item(
    Item={
        "_id":str(_id),
        "type":str(type),
        "upvotes":str(upvotes),
         }
    )

    print("Done")

for element in abcd['all']:
    id=element['_id']
    type = element['type']
    upvotes = element['upvotes']
    store_dynamo_db(id,type,upvotes)
