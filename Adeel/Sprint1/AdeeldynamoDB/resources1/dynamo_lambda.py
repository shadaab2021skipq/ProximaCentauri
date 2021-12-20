import boto3
import os

def lambda_handler(events, context):
    DB = boto3.resource('dynamodb')
    message = events['Records'][0]['Sns']['Message']
    reason = events['Records'][0]['Sns']['Reason for State Change']
    time = events['Records'][0]['Sns']['Timestamp']

    table_name = DB.Table('AdeeldynamoDbStack-TableCD117FA1-7FX8MT52I020')
    values = {}
    values['id'] = message
    values['Reason']= reason
    values['time']=time
    table_name.put_item(
    Item = values)