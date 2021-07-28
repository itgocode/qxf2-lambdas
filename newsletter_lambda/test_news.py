import boto3
from moto import mock_sqs
import daily_messages
 
@mock_sqs
def test_write_message_valid():
    "Test the write_message method with a valid message"
    sqs = boto3.resource('sqs')
    queue = sqs.create_queue(QueueName='test-skype-sender')
    daily_messages.QUEUE_URL = queue.url
    skype_message = 'Testing with a valid message'
    channel = 'test'
    expected_message = str({'msg':f'{skype_message}', 'channel':channel})
    daily_messages.write_message(skype_message, channel)
    sqs_messages = queue.receive_messages()
    assert sqs_messages[0].body == expected_message, 'Message in skype-sender does not match expected'
    print(f'The message in skype-sender SQS matches what we sent')
    assert len(sqs_messages) == 1, 'Expected exactly one message in SQS'
    print(f'\nExactly one message in skype-sender SQS')