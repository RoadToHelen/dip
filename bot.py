import random
from random import randrange
import datetime
import requests
from pprint import pprint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
# from database import create_db, create_users

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
                    sex = i.get('sex')
                    relation = i.get('relation')
                    city = i.get('city')
                    if 'city' in key:
                        city = key.get('city')
                        title = str(city.get('title'))
                        return title
                    user_dict = {'first_name': first_name, 'last_name': last_name, 'bdate': bdate, 'city': str(city.get('title')), 'sex': sex, 'relation': relation}
                    return user_dict
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def get_daiting_user_info(self, user_id):
        param = {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'}
        method = 'users.get'
        rec = requests.get(url=f'https://api.vk.com/method/{method}', params=param)
        response = rec.json()
        dict_user_info = response['response']
        try:
            for i in dict_user_info:
                for key, value in i.items():
                    bdate = i.get('bdate')
                    bdate_list = bdate.split('.')
                    if len(bdate_list) == 3:
                        bday = int(bdate_list[0])
                        bmonth = int(bdate_list[1])
                        byear = int(bdate_list[2])
                        day_today = int(datetime.date.today().day)
                        month_today = int(datetime.date.today().month)
                        year_today = int(datetime.date.today().year)
                        if month_today > bmonth:
                            age = year_today - byear
                        elif (month_today == bmonth and bday > day_today) or (month_today == bmonth and bday > day_today):
                            age = year_today - byear
                        else:
                            age = year_today - byear - 1
                    elif len(bdate_list) == 2 or None:
                        self.send_some_msg(user_id, 'Введите свою дату рождения в формате дд.мм.гггг: ')
                        for event in self.longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                bdate = event.text
                                bdate_list = bdate.split('.')
                                bday = int(bdate_list[0])
                                bmonth = int(bdate_list[1])
                                byear = int(bdate_list[2])
                                day_today = int(datetime.date.today().day)
                                month_today = int(datetime.date.today().month)
                                year_today = int(datetime.date.today().year)
                                if month_today > bmonth:
                                    age = year_today - byear
                                elif (month_today == bmonth and bday > day_today) or (month_today == bmonth and bday > day_today):
                                    age = year_today - byear
                                else:
                                    age = year_today - byear - 1
                                    print(age)#Почему выходит из ветки?
                    else:
                        self.send_some_msg(user_id, 'Ошибка')
                    sex = i.get('sex')
                    if sex == 1:
                        sex_name = 'мужчину'
                        sex_find = 2
                    elif sex == 2:
                        sex_name = 'женщину'
                        sex_find = 1
                    else:
                        VkBot.send_some_msg(user_id, 'Ваш пол не задан, кого ищем (мужчину/женщину): ')
                        for event in self.longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                sex_name = event.text
                    city = i.get('city')
                    if 'city' in key:
                        city = key.get('city')
                        title = str(city.get('title'))
                        return title
                    dating_user_dict = {'age from': (age-5), 'age to': (age+5),'city': str(city.get('title')), 'sex': sex_name, 'sex_find': sex_find}
                    # return dating_user_dict
                    return f"ищем {dating_user_dict['sex']} от {dating_user_dict['age from']} до {dating_user_dict['age to']} лет из города {dating_user_dict['city']}? Если параметры подходят - набери Да"
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def get_daiting_user(self, user_id):
        param = {'access_token': user_token, 'age_from': 18, 'age_to': 65, 'fields': 'bdate, sex, city, relation', 'count': 10, 'v': '5.131'}
        method = 'users.search'
        rec = requests.get(url=f'https://api.vk.com/method/{method}', params=param)
        response = rec.json()
        daiting_user = response['response']
        # du_list = daiting_user['items']
        # pprint(du_list)
        try:
            for i in daiting_user:
                for key, value in i.items():
                    id = i.get('id')
                    first_name = i.get('first_name')
                    last_name = i.get('last_name')
                    is_closed = i.get('is_closed')
                    bdate = i.get('bdate')
                    bdate_list = bdate.split('.')
                    relation = i.get('relation')
                    sex = i.get('sex')
                    # city = i.get('city')
                    # if 'city' in key:
                    #     city = key.get('city')
                    #     title = str(city.get('title'))
                    if is_closed == False and len(bdate_list) == 3 and (relation == 1 or relation == 6):
                        # self.get_daiting_sex(user_id):
                        dating_dict = {'id': id, 'first_name': first_name, 'last_name': last_name}
                        # 'city': str(city.get('title'))
                        pprint(dating_dict)
                        return f'{first_name} {last_name}'
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

VkBot = VkBot()


for event in VkBot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        request = event.text.lower()
        user_id = str(event.user_id)
        if request == 'привет':
            VkBot.send_some_msg(user_id, f'Привет, {VkBot.get_user_name(user_id)}! Если хочешь подобрать пару - набери "начать поиск"')
        # elif request == 'start search':
        #     VkBot.send_some_msg(user_id, f'Start searching for {VkBot.get_user_info(user_id)}')
        elif request == 'начать поиск':
            VkBot.send_some_msg(user_id, f'{VkBot.get_user_name(user_id)}, {VkBot.get_daiting_user_info(user_id)}')
        elif request == 'да':
            VkBot.send_some_msg(user_id, f'{VkBot.get_user_name(user_id)}, {VkBot.get_daiting_user(user_id)}')
        elif request == 'нет':
            VkBot.send_some_msg(user_id, f'{VkBot.get_user_name(user_id)}, очень жаль, до новых встреч!')
        #     # create_db
        else:
            VkBot.send_some_msg(user_id, f'{VkBot.get_user_name(user_id)}, твое сообщение не понятно') #pprint не влияет на выдачу в ВК
