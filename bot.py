import random
from random import randrange
import datetime
import requests
from pprint import pprint
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


class VkBot:
    def __init__(self):
        self.vk = vk_api.VkApi(token=group_token)
        self.vk2 = vk_api.VkApi(token=user_token)
        self.longpoll = VkLongPoll(self.vk)

    def send_some_msg(self, user_id, some_text):
        self.vk.method('messages.send', {'user_id': user_id, 'message': some_text, 'random_id': randrange(10**7)})


VkBot = VkBot()


# class VkUser:
#     url = 'https://api.vk.com/method/'
#
#     def __init__(self, user_token, user_id, version):
#         self.params = {'access_token': user_token,
#                        'user_ids': user_id,
#                        'v': version
#                        }


def get_user_info(user_id):
    param = {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'}
    method = 'users.get'
    rec = requests.get(url=f'https://api.vk.com/method/{method}', params=param)
    response = rec.json()
    dict_user_info = response['response']
    pprint(dict_user_info)


def get_user_name(user_id):
    param = {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'}
    method = 'users.get'
    rec = requests.get(url=f'https://api.vk.com/method/{method}', params=param)
    response = rec.json()
    dict_user_info = response['response']
    pprint(dict_user_info)
    try:
        for i in dict_user_info:
            for key, value in i.items():
                first_name = i.get('first_name')
                return first_name
    except KeyError:
        VkBot.send_some_msg(user_id, 'Ошибка')


for event in VkBot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        request = event.text.lower()
        user_id = str(event.user_id)
        if msg == 'hi':
            VkBot.send_some_msg(user_id, f'Hi, {get_user_name(user_id)}, if you want to pick up a pair - type  "start search"')
        elif request == 'привет':
            VkBot.send_some_msg(user_id, f'Привет, {get_user_name(user_id)}! Если хочешь подобрать пару - набери "начать поиск"')
        elif request == 'start search':
            VkBot.send_some_msg(user_id, f'Start searching')
        elif request == 'начать поиск':
            VkBot.send_some_msg(user_id, f'{get_user_name(user_id)}, начинаю поиск')
        else:
            VkBot.send_some_msg(user_id, f'{get_user_name(user_id)}, твое сообщение не понятно')
