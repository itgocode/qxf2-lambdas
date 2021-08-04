"""
Get messages for employees from pto-detector SQS
And post to Skype Sender if the message is a PTO message
"""
import json
import os
import boto3
import requests
import re
import wk12urlftr.conf as conf

#IS_PTO_URL = 'https://practice-testing-ai-ml.qxf2.com/is-pto'
QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/285993504765/skype-sender'

# create lambda client
client = boto3.client('lambda',
                        region_name= conf.region,
                        aws_access_key_id=conf.aws_access_key_id,
                        aws_secret_access_key=conf.aws_secret_access_key)

def clean_message(message):
    "Clean up the message received"
    message = message.replace("'", '-')
    message = message.replace('"', '-')

    return message
def URL_filter(msgs):
    URL_data = [] # list of lists
  
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,msgs)
    return [x[0] for x in url]

def get_message_contents(event):
    "Retrieve the message contents from the SQS event"
    record = event.get('Records')[0]
    message = record.get('body')
    message = json.loads(message)['Message']
    message = json.loads(message)

    return message

def post_newsletter_url(final_url):
    print("hello")

def lambda_handler(event, context):
    "Lambda entry point"
    message_contents = get_message_contents(event)
    message = message_contents['msg']
    channel = message_contents['chat_id']
    user = message_contents['user_id']
    print(f'{message}, {user}, {channel}')

    if channel == os.environ.get('ETC_CHANNEL') and user != os.environ.get('Qxf2Bot_USER'):
        cleaned_message = clean_message(message)
        final_url = URL_filter(cleaned_message)
        if final_url:
            response = post_newsletter_url(final_url)
        else:
            print("no url")
    else:
        print("message not found in etc channel")
