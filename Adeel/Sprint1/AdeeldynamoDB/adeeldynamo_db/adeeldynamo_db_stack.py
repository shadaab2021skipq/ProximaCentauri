from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as event_,
    aws_events_targets as targets_,
    aws_iam,
    aws_cloudwatch as cloudwatch_,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as actions_,
    aws_dynamodb as db
)
from constructs import Construct
from resources1 import constants1 as constants

class AdeeldynamoDbStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role= self.create_lambda_role()
        # The code that defines your stack goes here
        WH_lamda = self.create_lambda('FirstHellammbda',"./resources1",'WAMangoDBlambda.lambda_handler',lambda_role)
        SB_lamda = self.create_lambda('bucketHellammbda',"./resources1",'lambda_bucket.lambda_handler',lambda_role)
        db_lamda = self.create_lambda('secondHellammbda',"./resources1",'dynamo_lambda.lambda_handler',lambda_role)
         
         
        lambda_schedule = event_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler = WH_lamda)
        our_rule = event_.Rule(self, id = "MonitorWebHealthMAtrix",enabled = True, schedule= lambda_schedule,targets = [lambda_target] )
        
        
        #dynamo_table = self.create_table()
        dynamo_table = db.Table.from_table_arn(self,'ImportedTable','arn:aws:dynamodb:us-east-2:315997497220:table/AdeeldynamoDbStack-TableCD117FA1-1GHRSKAE7YTXG')
        dynamo_table.grant_read_write_data(lambda_role)
        
        
        
        topic = sns.Topic(self,'WHtopic')
        topic.add_subscription(subscriptions_.EmailSubscription('adeel.shahzad.s@skipq.org'))
        topic.add_subscription(subscriptions_.LambdaSubscription(fn=db_lamda)) 
        
        dimension={'URL': constants.URL_TO_MONITOR}
        availability_matric=cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,metric_name = constants.URL_MONITOR_NAME_AVAILABILITY,dimensions_map=dimension,period=cdk.Duration.minutes(1))
        availability_alarm= cloudwatch_.Alarm(self,
        id = 'AvailabilityAlarm',
        metric = availability_matric,
        comparison_operator= cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods = 1,
        threshold = 1
        )


        latency_matric=cloudwatch_.Metric(namespace=constants.URL_MONITOR_NAMESPACE,metric_name = constants.URL_MONITOR_NAME_LATENCY,dimensions_map=dimension,period=cdk.Duration.minutes(1))
        latency_alarm= cloudwatch_.Alarm(self,
        id = 'LatencyAlarm',
        metric = latency_matric,
        comparison_operator= cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
        datapoints_to_alarm=1,
        evaluation_periods = 1,
        threshold = 0.28
        )
        
        availability_alarm.add_alarm_action(actions_.SnsAction(topic))
        latency_alarm.add_alarm_action(actions_.SnsAction(topic))
        
    def create_lambda_role(self):
        lambdaRole = aws_iam.Role(self,"lambda-role",
        assumed_by = aws_iam.ServicePrincipal('lambda.amazonaws.com'),
        managed_policies = [aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"), 
        aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess")
        ])
        return lambdaRole
        
        
    def create_lambda(self,id, asset, handler,role):
        return lambda_.Function(self, id,
        code = lambda_.Code.from_asset(asset),
        handler=handler,
        runtime= lambda_.Runtime.PYTHON_3_6,
        role=role
    )
    def create_table(self):
        return db.Table(self,"Table",
        partition_key=db.Attribute(name="id", type=db.AttributeType.STRING))