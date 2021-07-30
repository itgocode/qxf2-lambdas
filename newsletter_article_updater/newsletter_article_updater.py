"""
This script will get messages from Qxf2 Skype channel: etc etc etc and parse the urls and
post it into newsletters database.
"""
import boto3
import json
import os
import re
import requests

QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/285993504765/skype-sender'

def clean_message(message):
    "Clean up the message received"
    message = message.replace("'", '-')
    message = message.replace('"', '-')

    return message

def get_message_contents(event):
    "Retrieve the message contents from the SQS event"
    record = event.get('Records')[0]
    message = record.get('body')
    message = json.loads(message)['Message']
    message = json.loads(message)

    return message

def parse_urls_from_message(message):
    "parse urls from message"
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, message)

    return [x[0] for x in url]

def write_message(message, channel):
    "Send a message to Skype Sender"
    sqs = boto3.client('sqs')
    message = str({'msg':f'{message}', 'channel':channel})
    sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=(message))

def lambda_handler(event, context):
    "Lambda entry point"
    message_contents = get_message_contents(event)
    message = message_contents['msg']
    channel = message_contents['chat_id']
    user = message_contents['user_id']
    print (f'{message}, {user}, {channel}')

    if channel == os.environ.get('CHANNEL_ID') and user != os.environ.get('Qxf2Bot_USER'):
        cleaned_message = clean_message(message)
        urls = parse_urls_from_message(cleaned_message)
        print ("Parsed urls:",urls)
        if urls != []:
            for url in urls:
                dump_url = json.dumps(url)
                #We need to modify post call as per auth design, may be we need to add new method for making call
                response = requests.post(url = os.environ.get('API_ENDPOINT'), data = dump_url, auth = '<auth_key>', header = {'Content-Type': 'application/json'})
                if response.status_code == 200:
                    print ('Url added to newsletter database')
                    #post message on Skype channel using skype sender for conformation
                    message_to_send = f'Added url to newsletter database {url}'
                    write_message(message_to_send, os.environ.get('CHANNEL_ID'))
                if response.status_code == 409:
                    print ('Url already exist in newsletter database')
                    #post message on Skype channel using skype sender for conformation
                    message_to_send = f'Url already exist in newsletter database {url}'
                    write_message(message_to_send, os.environ.get('CHANNEL_ID'))
       
        else:
            print("No URL found")
    else:
        print("Message not from expected channel")

