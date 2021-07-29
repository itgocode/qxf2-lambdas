"""
tests for the skype url fetcher
"""
import os
import sys
import unittest
from unittest import mock
from unittest.mock import patch
from skype_url_fetcher import lambda_handler
import conf as conf

class Test_skype_url_filter(unittest.TestCase):
    "Test class for skype url fetcher lambda"

    @patch('skype_url_fetcher.fetch_env_variables')
    def test_skype_url_fetcher_lambda_success(self, mock_env):
        "Test to check if the lambda posts the url if message contains an url"

        event = {"Records": [{"body": "{\"Message\":\"{\\\"msg\\\": \\\"Test: https://www.testurl.com\\\", \\\"chat_id\\\": \\\"19:626bd82f2bf249e788091763f2042b87@thread.skype\\\", \\\"user_id\\\":\\\"blah\\\"}\"}"}]}
        mock_env.return_value = conf.ETC_CHANNEL,conf.API

        # Assertion
        assert lambda_handler(event=event,context=None) == "Success"

    @patch('skype_url_fetcher.fetch_env_variables')
    def test_skype_url_fetcher_lambda_failure(self, mock_env):
        "Test to check if the lambda returns no url found if message doesn't contain any url"

        event = {"Records": [{"body": "{\"Message\":\"{\\\"msg\\\": \\\"Test: test message\\\", \\\"chat_id\\\": \\\"19:626bd82f2bf249e788091763f2042b87@thread.skype\\\", \\\"user_id\\\":\\\"blah\\\"}\"}"}]}
        mock_env.return_value = conf.ETC_CHANNEL,conf.API

        # Assertion
        assert lambda_handler(event=event,context=None) == "No url found"

if __name__=="__main__":
    unittest.main()