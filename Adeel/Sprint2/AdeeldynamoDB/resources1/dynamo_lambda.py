import boto3,os
import json

client = boto3.client('dynamodb')
  
  
   ############################## Creating object for table  ###############################
  
def lambda_handler(event, context):
   # db = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    message = event['Records'][0]['Sns']
    msg = json.loads(message['Message'])
    #table_name = db.Table('AdeelAlarm')
    record = event['Records'][0]['dynamodb']
    arnText = record['eventSourceARN']
    listof = arnText.split('/')
    index = listof.index('stream')
    table_name = listof[index-1]

     ############################## Putting values in dynamo table###############################
    #table_name=os.getenv('table_name')
    client.put_item(
    TableName = table_name,
    Item={
        'Timestamp':{'S' : message['Timestamp']},
        'Reason':{'S':msg['NewStateReason']}
    })