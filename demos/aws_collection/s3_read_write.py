"""Collection"""

import asyncio
from asyncio import tasks
from prefect import task, flow
from prefect_aws import AwsCredentials
from prefect_aws.s3 import S3Bucket
from prefect_aws.s3 import s3_list_objects
from prefect.blocks.notifications import SlackWebhook


@flow(name="Subflow- Get Bucket Objs")
async def get_bucket_objects():

    aws_creds_block = await AwsCredentials.load("my-aws-creds-block")

    s3_bucket_objs = await s3_list_objects(
        bucket="sales-eng-beta-blocks",
        aws_credentials=aws_creds_block
    )

    obj_keys = [obj['Key'] for obj in s3_bucket_objs]

    return obj_keys


@flow(name="AWS S3 Bucket Roundtrip")
async def aws_s3_bucket_roundtrip():

    s3_bucket_block = await S3Bucket.load("my-s3-bucket-block")

    s3_bucket_objs = await get_bucket_objects()

    await s3_bucket_block.write_path("my_file.csv", content=b"Hello from Prefect!")
    
    bucket_file_path = "recipes/flows-advanced/blocks/my_file.csv"

    file_contents = await s3_bucket_block.read_path(bucket_file_path)

    if len(file_contents.decode()) == 0:
        slack_webhook_block = SlackWebhook.load("slack-notification")
        slack_webhook_block.notify("Your file is empty!!")

    print(file_contents.decode())

if __name__ == "__main__":

    asyncio.run(aws_s3_bucket_roundtrip())