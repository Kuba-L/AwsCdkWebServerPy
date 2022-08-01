import aws_cdk as cdk

from stack.vpc import VpcStack
from stack.ec2 import Ec2Stack


app = cdk.App()
vpc_stack = VpcStack(app, "VpcStack")
ec2_stack = Ec2Stack(app, "Ec2Stack", vpc=vpc_stack.vpc)

app.synth()
