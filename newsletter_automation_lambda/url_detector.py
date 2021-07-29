"""
a) filter messages on etc,etc,etc by getting messages from Skype Listener SNS
b) write something to spot URLs - https://www.geeksforgeeks.org/python-check-url-string/
c) insert URL via an API call
"""

from skpy import Skype
import skype_config as sc
import skype_credentials as cred
import re

def read_skype_messages():
    # a) filter messages on etc,etc,etc by getting messages from Skype Listener SNS
    sk = Skype(cred.skype_username, cred.skype_password)
    channel = sk.chats.chat(sc.channel_id)
    return channel.getMsgs()


def filter_skype_messages(event):
    # b) write something to spot URLs - https://www.geeksforgeeks.org/python-check-url-string/
    for msg in event:
        url_filter = re.search(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", str(msg))
        
        if url_filter:
            print ('\n Message is :\n{}'.format(msg))            
            print('\n Posted link is : {}'.format(url_filter))
        
if __name__ == "__main__":
    messages = read_skype_messages()
    filter_skype_messages(messages)
