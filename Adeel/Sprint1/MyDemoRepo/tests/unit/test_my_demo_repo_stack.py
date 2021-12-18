import aws_cdk as core
import aws_cdk.assertions as assertions

from my_demo_repo.my_demo_repo_stack import MyDemoRepoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_demo_repo/my_demo_repo_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyDemoRepoStack(app, "my-demo-repo")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
