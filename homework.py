import time
import os

import requests

from twilio.rest import Client

from dotenv import load_dotenv
load_dotenv()

BASE_URL = 'https://api.vk.com/method/users.get'
API_V = '5.92'

secret_twilio_token = os.getenv('TWILIO_TOKEN')
account_sid = os.getenv('ACCOUNT_SID')
access_token = os.getenv('ACCESS_TOKEN')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')

client = Client(account_sid, secret_twilio_token)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': API_V,
        'access_token': access_token
    }
    user_status = requests.post(BASE_URL, params=params)
    return user_status.json()['response'][0]['online']


def send_sms(sms_text):
    message = client.messages.create(
                            body=sms_text,
                            from_=number_from,
                            to=number_to
                        )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
