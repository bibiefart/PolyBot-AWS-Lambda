import json
import boto3
from loguru import logger
from utils import search_download_youtube_video
import logging
from botocore.exceptions import ClientError
import os

with open('config.json') as f:
    config = json.load(f)

sqs = boto3.resource('sqs', region_name=config.get('aws_region'))
queue = sqs.get_queue_by_name(QueueName=config.get('bot_to_worker_queue_name'))

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def process_msg(msg):
    locations = search_download_youtube_video(msg)
    file_name = f"./{locations[0]}"
    bucket = "bibi-s3-v2"
    upload_file(file_name, bucket)

    # TODO upload the downloaded video to your S3 bucket


def lambda_handler(event, context):
    logger.info(f'New event {event}')
    sqs = boto3.resource('sqs', region_name=config.get('aws_region'))
    workers_queue = sqs.get_queue_by_name(QueueName=config.get('bot_to_worker_queue_name'))
    #sqs = boto3.resource('sqs')
    #workers_queue = sqs.get_queue_by_name(QueueName='bibi-sqs-for-lamda-polybot')
    for message in workers_queue.receive_messages(MessageAttributeNames=['Author']):
        process_msg(message.body)

    # TODO complete the code that processes all records (use use process_msg())
