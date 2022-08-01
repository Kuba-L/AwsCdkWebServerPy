import aws_cdk as cdk

from stack.vpc import VpcStack
from stack.s3 import S3Stack
from stack.ec2 import Ec2Stack


app = cdk.App()
vpc_stack = VpcStack(app, "VpcStack")
s3_stack = S3Stack(app, "S3Stack")
ec2_stack = Ec2Stack(app, "Ec2Stack", vpc=vpc_stack.vpc)
ec2_stack.add_dependency(s3_stack)

app.synth()
