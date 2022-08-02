import aws_cdk as cdk

from stack.vpc import VpcStack
from stack.s3 import S3Stack
from stack.ec2 import Ec2Stack
from stack.r53 import R53Stack


app = cdk.App()
vpc_stack = VpcStack(app, "VpcStack")
s3_stack = S3Stack(app, "S3Stack")
ec2_stack = Ec2Stack(app, "Ec2Stack", vpc=vpc_stack.vpc, bucket=s3_stack.artifacts_bucket)
ec2_stack.add_dependency(s3_stack)
# r53_stack = R53Stack(app, "R53Stack", elb=ec2_stack.alb)

app.synth()
