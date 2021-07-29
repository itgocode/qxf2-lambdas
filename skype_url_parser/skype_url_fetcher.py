"""
Lambda to fetch and filter the urls posted on skype
"""
import json
import os
import re
import requests

def get_message_contents(event):
    "Retrieve the message contents from the SQS event"
    record = event.get('Records')[0]
    message = record.get('body')
    message = json.loads(message)['Message']
    message = json.loads(message)

    return message

def check_url(message):
    "Fetch the urls from a message, returns empty list if no url found"
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    return url

def fetch_env_variables():
    "Get the environment variables"
    channel = os.environ.get('ETC_CHANNEL')
    api_endpoint = os.environ.get('API')
    return channel,api_endpoint

def lambda_handler(event, context):
    "Lambda entry point"
    message_contents = get_message_contents(event)
    message = message_contents['msg']
    channel = message_contents['chat_id']
    user = message_contents['user_id']
    print(f'{message}, {user}, {channel}')

    if channel == fetch_env_variables()[0]:
        url = check_url(message)
        if url:
            print(url)
            jsonified_url = json.dumps(url)
            api_endpoint = fetch_env_variables()[1]
            post_url = requests.post(url = api_endpoint, data = jsonified_url)
            if post_url.status_code == 200:
                return "Success"
            else:
                return "Failed"


        else:
            return "No url found"