"""
Get messages for employees from pto-detector SQS
And post to Skype Sender if the message is a PTO message
"""
import json
import os
import boto3
import requests
#IS_PTO_URL = 'https://practice-testing-ai-ml.qxf2.com/is-pto'
QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/285993504765/skype-sender'


def clean_message(message):
    "Clean up the message received"
    message = message.replace("'", '-')
    message = message.replace('"', '-')

    return message

def get_is_pto(message):
    "Check if the message is a PTO message"
    response = requests.post(url=IS_PTO_URL,data={'message':message})
    result_flag = response.json()['score'] == 1

    return result_flag


def get_message_contents():
    "Retrieve the message contents from the SQS event"
    record = event.get('Records')[0]
    message = record.get('body')
    message = json.loads(message)['Message']
    message = json.loads(message)
    print (message)

    return message

def lambda_handler(event, context):

    "Lambda entry point"
    message_contents = get_message_contents()
    message = message_contents['msg']
    channel = message_contents['chat_id']
    user = message_contents['user_id']
    print(f'{message}, {user}, {channel}')
    is_pto_flag = False
    if channel == os.environ.get('PTO_CHANNEL') and user != os.environ.get('Qxf2Bot_USER'):
        cleaned_message = clean_message(message)
        #is_pto_flag = get_is_pto(cleaned_message)
        print(f'{is_pto_flag}')
   



    
