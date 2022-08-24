"""Collection Define Blocks"""
from prefect_aws import AwsCredentials
from prefect_aws.s3 import S3Bucket

# Load Env Vars
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Instantiate and Save Blocks to Orion API

my_aws_creds_block = AwsCredentials(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
my_aws_creds_block.save('my-aws-creds-block', overwrite=True)

my_s3_bucket_block = S3Bucket(
        bucket_name="sales-eng-beta-blocks",  # must exist
        aws_credentials=my_aws_creds_block,
        basepath="recipes/flows-advanced/blocks/",
    )

print(my_s3_bucket_block.get_block_type_slug())

my_s3_bucket_block.save('my-s3-bucket-block', overwrite=True)
