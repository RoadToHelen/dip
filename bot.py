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

    def get_user_name(self, user_id):
        param = {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'}
        method = 'users.get'
        rec = requests.get(url=f'https://api.vk.com/method/{method}', params=param)
        response = rec.json()
        dict_user_info = response['response']
        try:
            for i in dict_user_info:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    return first_name
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def get_user_info(self, user_id):
        param = {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'}
        method = 'users.get'
        rec = requests.get(url=f'https://api.vk.com/method/{method}', params=param)
        response = rec.json()
        dict_user_info = response['response']
        try:
            for i in dict_user_info:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    last_name = i.get('last_name')
                    bdate = i.get('bdate')
                    city = i.get('city')
                    sex = i.get('sex')
                    relation = i.get('relation')
                    user_dict = {'first_name': first_name, 'last_name': last_name, 'bdate': bdate, 'city': city, 'sex': sex, 'relation': relation}
                    return user_dict
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')


VkBot = VkBot()


for event in VkBot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        request = event.text.lower()
        user_id = str(event.user_id)
        if msg == 'hi':
            VkBot.send_some_msg(user_id, f'Hi, {VkBot.get_user_name(user_id)}, if you want to pick up a pair - type  "start search"')
        elif request == 'привет':
            VkBot.send_some_msg(user_id, f'Привет, {VkBot.get_user_name(user_id)}! Если хочешь подобрать пару - набери "начать поиск"')
        elif request == 'start search':
            VkBot.send_some_msg(user_id, f'Start searching for {VkBot.get_user_info(user_id)}')
        elif request == 'начать поиск':
            VkBot.send_some_msg(user_id, f'{VkBot.get_user_name(user_id)}, начинаю поиск по параметрам {VkBot.get_user_info(user_id)}')
        else:
            VkBot.send_some_msg(user_id, f'{VkBot.get_user_name(user_id)}, твое сообщение не понятно')
