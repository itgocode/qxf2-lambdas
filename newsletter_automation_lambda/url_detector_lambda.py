"""
a) filter messages on etc,etc,etc by getting messages from Skype Listener SNS
b) write something to spot URLs - https://www.geeksforgeeks.org/python-check-url-string/
c) insert URL via an API call
"""
import json
import boto3
import requests

QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/285993504765/skype-sender'

from skpy import Skype
import skype_config as sc
import skype_credentials as cred
import re

def lambda_handler(event, context):
    "Lambda entry point"
    message_contents = get_message_contents(event)
    message = message_contents['msg']
    channel = message_contents['chat_id']
    user = message_contents['user_id']
    print(f'{message}, {user}, {channel}')


def get_message_contents(event):
    #a) filter messages on etc,etc,etc by getting messages from Skype Listener SNS
    record = event.get('Records')[0]
    message = record.get('body')
    message = json.loads(message)['Message']
    message = json.loads(message)

    return message

def filter_skype_messages(event):
    #b) write something to spot URLs - https://www.geeksforgeeks.org/python-check-url-string/
    for msg in event:
        url_filter = re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", str(msg))
        
        if url_filter:
            print ('\n Message is :\n{}'.format(msg))            
            print('\n Posted link is : {}'.format(url_filter))
        

