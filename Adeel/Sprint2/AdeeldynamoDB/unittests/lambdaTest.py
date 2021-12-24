import pytest
from aws_cdk import core 

from adeeldynamo_db.adeeldynamo_db_stack import  AdeeldynamoDbStack
def lambda_test():
    app = core.app()
    AdeeldynamoDbStack(app, 'Stack')
    temp = app.synth().get_stack_by_name('Stack').template
    
    lambda_function = [resource for resource in temp['Resources'].values  if resource['type']=="AWS::S3::Bucket"]
    assert len(lambda_function)==1
    
