from aws_cdk import Stack
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_s3_deployment as s3_deployment
from constructs import Construct

class S3Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.artifacts_bucket = s3.Bucket(self, 'artifactsBucket',
                                bucket_name='artifacts-bucket-for-that-web-server-yup',
                                block_public_access=s3.BlockPublicAccess.BLOCK_ALL,  # type: ignore
                                )
                                

        self.artifacts_deployment = s3_deployment.BucketDeployment(self,'deployWebArtifact',
                                                                    destination_bucket=self.artifacts_bucket,
                                                                    sources=[s3_deployment.Source.asset('./www/')],
                                                                    )