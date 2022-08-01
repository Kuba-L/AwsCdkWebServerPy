from aws_cdk import Stack
import aws_cdk.aws_ec2 as ec2
from constructs import Construct



class Ec2Stack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        print(f"Using VPC: {vpc.vpc_id}") 