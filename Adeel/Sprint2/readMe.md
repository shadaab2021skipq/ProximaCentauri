Clone
First clone all the files from git hub repository using this command.
>>>git clone https://github.com/adeel2021skipq/ProximaCentauri.git
Go to project directory
>>>cd ProximaCentauri/Adeel/Sprint2/adeeldynamoDB

Virtual environment
Go to virtual environment using command
>>>source .venv/bin/activate
Bootstrap
Bootstrap the code using that command
>>>cdk bootstrap aws://315997497220/us-east-2 --qualifier <name> --toolkit-stack-name <toolkitname>
Deploy
>>>cdk deploy AdeelPipelineStack3