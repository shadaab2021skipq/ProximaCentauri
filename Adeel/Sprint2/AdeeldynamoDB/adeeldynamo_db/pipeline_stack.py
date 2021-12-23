##########################Importing All the nessearry libraries#######################################
from aws_cdk import core
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines
from adeeldynamo_db.dynamo_stage import DynamoStage
from adeeldynamo_db.adeeldynamo_db_stack import AdeeldynamoDbStack

class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        ############################## Pipelines Source ###############################
    
        source = pipelines.CodePipelineSource.git_hub(repo_string='adeel2021skipq/ProximaCentauri' ,
        branch = 'main',authentication=core.SecretValue.secrets_manager('Adeel/github/token1'),
        trigger = cpactions.GitHubTrigger.POLL
        )
        
        ############################## Pipelines built ###############################
        
        
        synth = pipelines.ShellStep('synth',input = source,
        commands=["cd Adeel/Sprint2/AdeeldynamoDB","pip install -r requirements.txt" , "npm install -g aws-cdk","cdk synth"],
        primary_output_directory = "Adeel/Sprint2/AdeeldynamoDB/cdk.out")
        
        ############################## Pipelines update ###############################
        
        pipeline = pipelines.CodePipeline(self,'pipeline',synth = synth)
    
        beta = DynamoStage(self, "Beta" , env= {
            'account':'315997497220',
            'region': 'us-east-2'
        })
        pipeline.add_stage(beta)
    