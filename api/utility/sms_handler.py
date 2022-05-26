import os

import africastalking

username = 'praiseabarber'
api_key = os.environ.get('AFTK_API_KEY')
africastalking.initialize(username, api_key)

# initializing service for SMS
sms = africastalking.SMS


def send_sms(receiver_number, message_body):
    """
        Sends sms using africastalking API
    :param receiver_number: Phone number of receiver
    :param message_body: message content
    :return: None
    """
    response = sms.send(message_body, receiver_number)
    print(response)
