from aws_cdk import Stack
import aws_cdk.aws_route53 as r53
import aws_cdk.aws_route53_targets as targets
from constructs import Construct

class R53Stack(Stack):

    def __init__(self, scope: Construct, id: str, elb, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        public_hosted_zone = r53.PublicHostedZone(self, "HostedZone",zone_name="helloworld.cloud.test")

        r53.ARecord(self, "AliasRecord",
                        zone=public_hosted_zone,
                        target=r53.RecordTarget.from_alias(targets.LoadBalancerTarget(elb))
                    )