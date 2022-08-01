from aws_cdk import Stack
import aws_cdk.aws_iam as iam
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
from constructs import Construct

EC2_TYPE = "t2.micro"
LINUX_AMI = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )

with open("./user_data/user_data.sh") as f:
    user_data = f.read()

class Ec2Stack(Stack):

    def __init__(self, scope: Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        alb_sg = ec2.SecurityGroup(self, "alb-sg",vpc=vpc)
        # alb_sg.add_ingress_rule(ec2.Peer.ipv4("63.35.68.30/32"),
        #                         ec2.Port.tcp(80),
        #                         "allow priv ip")
        
        # for now from anywhere anyway
        alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(),
                                ec2.Port.tcp(80),
                                "allow from anywhere")

        alb = elb.ApplicationLoadBalancer(self, "alb",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="alb",
                                          security_group=alb_sg
                                          )

        listener = alb.add_listener("listening_on_80",
                                    port=80,
                                    open=True)

        # adding SSM to setup the web server
        role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))

        self.asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                instance_type=ec2.InstanceType(instance_type_identifier=EC2_TYPE),
                                                machine_image=LINUX_AMI,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=1,
                                                min_capacity=1,
                                                max_capacity=1,
                                                role=role # type: ignore
                                                )

        self.asg.scale_on_schedule("ScaleUpAt14",
            schedule=autoscaling.Schedule.cron(hour="14", minute="00"),
            time_zone="CET",
            desired_capacity=2,
            min_capacity=2,
            max_capacity=2,
        )

        self.asg.scale_on_schedule("ScaleDownAt18",
            schedule=autoscaling.Schedule.cron(hour="18", minute="00"),
            time_zone="CET",
            desired_capacity=1,
            min_capacity=1,
            max_capacity=1,
        )

        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")

        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])