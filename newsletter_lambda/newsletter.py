"""
Get messages for employees from pto-detector SQS
And post to Skype Sender if the message is a PTO message
"""
import json
import os
import boto3
import requests
from urlextract import URLExtract
#IS_PTO_URL = 'https://practice-testing-ai-ml.qxf2.com/is-pto'
QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/285993504765/skype-sender'

def get_url_from_message(message):
        extractor = URLExtract()
        urls = extractor.find_urls(message)
        
        #url_extract = re.findall(r'(https?://\S+)', message)
        print("URL on extract",urls[0])
        return (urls[0])

def clean_message(message):
    "Clean up the message received"
    message = message.replace("'", '-')
    message = message.replace('"', '-')

    return message



def get_message_contents(event):
    "Retrieve the message contents from the SQS event"
    print("Empty message")
    record = event.get('Records')[0]
    message = record.get('body')
    message = json.loads(message)['Message']
    message = json.loads(message)
    print (message)

    return message

def lambda_handler(event, context):
    "Lambda entry point"
    
    message_contents = get_message_contents(event)
    message = message_contents['msg']
    channel = message_contents['chat_id']
    user = message_contents['user_id']
    print(f'{message}, {user}, {channel}')
    is_pto_flag = False
    if channel == os.environ.get('ETC_CHANNEL'):
        print("Inside the Channel")
        cleaned_message = clean_message(message)
        url = get_url_from_message(message)
        print ("one url only",url)



    
