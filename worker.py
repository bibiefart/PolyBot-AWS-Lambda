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
    cmd = "rm -rf /tmp/*"
    returned_value = os.system(cmd)  # returns the exit code in unix
    logger.info('returned value:', returned_value)
    logger.info(f'processing msg')
    locations = search_download_youtube_video(msg)
    logger.info(f'locations {locations}')
    file_name = f"{locations[0]}"
    bucket = "bibi-s3-v3"
    logger.info(f'File To Upload {file_name}')
    head, tail = os.path.split(f"{file_name}")
    upload_file(file_name, bucket, tail)

    # TODO upload the downloaded video to your S3 bucket


def lambda_handler(event, context):
    logger.info(f'New event {event}')
    #sqs = boto3.resource('sqs', region_name=config.get('aws_region'))
    #workers_queue = sqs.get_queue_by_name(QueueName=config.get('bot_to_worker_queue_name'))
    #sqs = boto3.resource('sqs')
    #workers_queue = sqs.get_queue_by_name(QueueName='bibi-sqs-for-lamda-polybot')
    #for message in workers_queue.receive_messages(MessageAttributeNames=['chat_id']):
    #    logger.info(f'Message Body {message.body}')
    #    process_msg(message.body)

    # try:
    #     messages = workers_queue.receive_messages(
    #         MessageAttributeNames=['All'],
    #         MaxNumberOfMessages=10,
    #         WaitTimeSeconds=2
    #     )
    #     logger.info(f'THE MESSAGES: {messages}')
    #     for msg in messages:
    #         print("Received message: %s: %s", msg.message_id, msg.body)
    #         logger.info("Received message: %s: %s", msg.message_id, msg.body)
    #         process_msg(msg.body)
    # except ClientError as error:
    #     logger.exception("Couldn't receive messages from queue: %s", queue)
    #     raise error

    for record in event['Records']:
        logger.info(f'THE record: {record}')
        body = record['body']
        logger.info(f'THE body: {body}')
        process_msg(body)

    # TODO complete the code that processes all records (use use process_msg())
    # response = sqs.receive_message(
    #     QueueUrl=config.get('queue_url'),
    #     MaxNumberOfMessages=1,
    #     WaitTimeSeconds=10,
    # )
    # logger.info(f"Number of messages received: {len(response.get('Messages', []))}")
    # for message in response.get("Messages", []):
    #     message_body = message["Body"]
    #     process_msg(message_body)
    #     logger.info(f"Message body: {json.loads(message_body)}")

#lambda_handler('rrr', 'ccc')