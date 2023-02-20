import random
from random import randrange
import datetime
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
# from database import create_db

try:
    with open('group_token.txt', 'r') as file:
        group_token = file.read().strip()
    with open('user_token.txt', 'r') as file:
        user_token = file.read().strip()
except FileNotFoundError:
    group_token = input('group_token: ')
    user_token = input('user_token: ')


vk = vk_api.VkApi(token=group_token)
vk2 = vk_api.VkApi(token=user_token)
longpoll = VkLongPoll(vk)


def send_some_msg(user_id, some_text):
    vk.method('messages.send', {'user_id': user_id, 'message': some_text, 'random_id': randrange(10**7)})

def get_user_info(user_id):
    vk.method('users.get', {'user_ids': user_id, 'v': '5.131'})





for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        request = event.text.lower()
        user_id = str(event.user_id)
        if msg == 'hi':
            send_some_msg(user_id, f'Hi, {user_id}, if you want to pick up a pair - type  "start search"')
        elif request == 'привет':
            send_some_msg(user_id, f'Привет, {user_id}! Если хочешь подобрать пару - набери "начать поиск"')
        elif request == 'start search':
            send_some_msg(user_id, f'Start searching')
        elif request == 'начать поиск':
            send_some_msg(user_id, f'{user_id}, начинаю поиск')

        else:
            send_some_msg(user_id, f'{user_id}, твое сообщение не понятно')