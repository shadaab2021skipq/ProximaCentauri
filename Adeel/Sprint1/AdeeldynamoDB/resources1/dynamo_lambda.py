import boto3
import os

def lambda_handler(events, context):
    DB = boto3.resource('dynamodb')
    message = events['Records'][0]['Sns']['Message']
    table_name = DB.Table('AdeeldynamoDbStack-TableCD117FA1-1GHRSKAE7YTXG')
    values = {}
    values['id'] = message['AlarmName']
    values['Reason']= message['NewStateReason']
    values['Time']=message['StateCangeTime']
    table_name.put_item(
    Item=values)