"""
Lambda to
    buzz colleagues on their Raspberry Pi device,
    when a colleague wants to have water cooler conversations.
"""
import os
import requests

def get_participants_count():
    """
    Returns the participants count in the WaterCoolerTalks Jitsi room.
    """
    participants_count = 0
    try:
        response = requests.get(os.environ['JITSI_ROOM_SIZE_ENDPOINT'])
        if response.status_code == 200:
            participants_count = response.json()['participants']
        elif response.status_code == 404:
            print('\n No participants in room!')
    except requests.exceptions.RequestException as request_error:
        print(f'\n Request error: \n {request_error}')
        raise Exception ('Error while fetching info from Jitsi server!') from request_error
    except Exception as error:
        print(f'\n Error encountered: \n {error}')
        raise Exception('Error while fetching info from Jitsi server!') from error
    return participants_count

def buzz_colleagues(participants_count):
    """
    Buzz colleagues based on the status of buzz_flag, when the room has participants.
    """
    buzz_flag = False # Line should be removed and variable's state should be stored in AWS
    if participants_count > 0:
        if buzz_flag is False:
            # <TBD> Add code to integrate with Raspberry Pi and buzz colleagues.
            print('Buzzing colleagues to chit-chat!')
            buzz_flag = True
    else:
        buzz_flag = False

def lambda_handler(event, context):
    "Lambda entry point."
    buzz_colleagues(get_participants_count())
