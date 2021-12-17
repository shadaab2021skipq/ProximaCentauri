from aws_cdk import (
    core as cdk,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam,
    aws_Cloudwatch as cloudwatch_
    )
from resource import constants as constants


class MyRepoTestStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
#create permission and roles for lambda
        lambda_role = self.create_lambda_role()
        
# The code that defines your stack goes here
        Hwlambda = self.create_lambda("web_health","./resources","web_health_lambda.lambda_handler",lambda_role)

#To Create Events, Set Target lambda, Set Rules of activation of events        
        lambda_schedule = events_.Schedule.rate(cdk.Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler=Hwlambda) ####To connect events to target lambda which is Hwlambda
        rule = events_.Rule(self, "web_health_lambda", description="Continue lambda", enabled = True, schedule=lambda_schedule,targets=[lambda_target]) 
        
# To set alarm        
        #set public metric
        dimension= {'Name' : 'URL','Value' : constants.URL_TO_MONITOR}
        availability_metric = cloudwatch_.Metric(nameSpace=constants.URL_NONITOR_NAMESPACE,metric_name=constants.URL_MONITOR_NAME_AVAILABILITY,dimensions_map=dimension)
        #alarm setup
        availability_alarm=cloudwatch_.Alarm(self, id='AvailabilityAlarm',
                                            metric=availability_metric,
                                            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
                                            datapoints_to_alarm=1,
                                            evaluation_periods=1,
                                            threshold=1)
        
#Function to create roles and permission for lambda     
    def create_lambda_role(self):
        lambdarole = aws_iam.Role(self, "lambda-role",
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
            managed_policies=[
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),    
                            aws_iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess')
                            ])
        return lambdarole
    
#Function to create a lambda
    def create_lambda(self, id, asset, handler, role): 
        return lambda_.Function(self, id,
            code=lambda_.Code.from_asset(asset),
            handler=handler,
            runtime=lambda_.Runtime.PYTHON_3_6, #### What is aws_lambda.Code.from_asset
            role = role
            )
        
        # example resource
        # queue = sqs.Queue(
        #     self, "MyRepoTestQueue",
        #     visibility_timeout=cdk.Duration.seconds(300),
        # )
