"""
Lambda to
    buzz colleagues on their raspberryPi device,
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
            print('No participants in room')
    except requests.exceptions.RequestException as request_error:
        print(f'Request error: \n {request_error}')
        raise Exception ('Error while fetching info from Jitsi server!') from request_error
    except Exception as error:
        print(f'Error encountered: \n {error}')
        raise Exception('Error while fetching info from Jitsi server!') from error
    return participants_count

def lambda_handler(event, context):
    "Lambda entry point."
    buzz_flag = False # Line should be removed and variable's state should be stored in AWS
    peers_count = get_participants_count()
    if peers_count > 0:
        if buzz_flag is False:
            # Add the code that integrates with raspberryPi to buzz colleagues here.
            print('Buzzing colleagues to chit-chat!')
            buzz_flag = True
    else:
        buzz_flag = False
