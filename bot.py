from random import randrange
import datetime
from pprint import pprint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError
from database import create_db, create_users, select_users, insert_users, drop_users, select_duser_ids, check_users


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

    def send_some_msg(self, user_id, some_text, attachment=None):
        self.vk.method('messages.send', {'user_id': user_id, 'message': some_text, 'random_id': randrange(10**7), 'attachment': attachment})

    def get_user_name(self, user_id):
        try:
            dict_user_name = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'v': '5.131'})
            for i in dict_user_name:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    return first_name
        except ApiError:
            return

    def get_user_id(self, user_id):
        try:
            dict_user_id = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'v': '5.131'})
            for i in dict_user_id:
                for key, value in i.items():
                    user = i.get('user_ids')
                    return user
        except ApiError:
            return

    def get_user_info(self, user_id):
        try:
            dict_user_info = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'})
            for i in dict_user_info:
                for key, value in i.items():
                    first_name = i.get('first_name')
                    last_name = i.get('last_name')
                    bdate = i.get('bdate')
                    sex = i.get('sex')
                    relation = i.get('relation')
                    city = i.get('city')
                    if (bdate != None) and (city != None) and (sex != None) and (relation != None):
                    # user_dict = {'first_name': first_name, 'last_name': last_name, 'bdate': bdate, 'city': str(city.get('title')), 'sex': sex, 'relation': relation}
                        user_list = [user_id, first_name, last_name, bdate, str(city.get('title')), sex, relation]
                        return user_list
                    else:
                        self.get_user_data(user_id)
        except ApiError:
            return

    def get_user_data(self, user_id):
        try:
            self.send_some_msg(user_id, f'{self.get_user_name(user_id)}, ищем возраст от (min = 18):')
            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    age_from = event.text
                    self.send_some_msg(user_id, f'{self.get_user_name(user_id)}, ищем возраст по:')
                    for event in self.longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            age_to = event.text
                            self.send_some_msg(user_id, f'{self.get_user_name(user_id)}, внесите город поиска:')
                            for event in self.longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    city = event.text
                            user_data = {'age_from': age_from, 'age_to': age_to, 'city': city}
                            return user_data
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def get_daiting_user_info(self, user_id):
        try:
            dict_duser_info = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'})
            for i in dict_duser_info:
                for key, value in i.items():
                    bdate = i.get('bdate')
                    bdate_list = bdate.split('.')
                    if len(bdate_list) == 2 or None:
                        age = self.get_bdate(user_id)
                    elif len(bdate_list) == 3:
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
                    dating_user_dict = {'age from': (age - 5), 'age to': (age + 5), 'city': str(city.get('title')),
                                        'sex': sex_name, 'sex_find': sex_find}
                    return self.send_some_msg(user_id, f"{self.get_user_name(user_id)}, ищем {dating_user_dict['sex']} от {dating_user_dict['age from']} до {dating_user_dict['age to']} лет из города {dating_user_dict['city']}?")
        except ApiError:
            return


#     def user_serch(self, user_id, offset=None):
#
#         try:
#             profiles = self.vk2.method('users.search',
#                                        {'access_token': user_token, 'sex': self.get_daiting_sex(user_id),
#                                         'relation': 1 or 6,
#                                         'age_from': self.get_age(user_id) - 5, 'age_to': self.get_age(user_id) + 5,
#                                         'friend_status': 0,
#                                         'has_photo': 1, 'offset': offset,
#                                         'fields': 'bdate, sex, city, relation', 'count': 30, 'v': '5.131'})
#
#         except ApiError:
#             return
#
#         profiles = profiles['items']
#
#         result = []
#         for profile in profiles:
#             if profile['is_closed'] == False:
#                 result.append({'name': profile['first_name'] + ' ' + profile['last_name'],
#                                'id': profile['id']
#                                })
#
#         return result
#
#
#
#     def get_profile_info(self, user_id):
#         info = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'})
#         return info
#
# if __name__ == '__main__':
#     tools = VkBot(access_token)
#     print(tools.get_profile_info(user_id))
#     info = tools.get_profile_info(789657038)
#     if info:
#         print(tools.get_profile_info(789657038))
#     else:
#         pass
#     profiles = tools.user_serch(1, 20, 40, 1)
#     print(profiles)

    def get_bdate(self, user_id):
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
                    return age

    def get_dating_sex(self, user_id):
        try:
            dating_sex_dict = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'fields': 'sex', 'v': '5.131'})
            for i in dating_sex_dict:
                for key, value in i.items():
                    sex = i.get('sex')
                    if sex == 1:
                        find = 2
                        return find
                    elif sex == 2:
                        find = 1
                        return find
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def get_age(self, user_id):
        try:
            age_dict = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate', 'v': '5.131'})
            for i in age_dict:
                for key, value in i.items():
                    bdate = i.get('bdate')
                    bdate_list = bdate.split('.')
                    if len(bdate_list) == 2 or None:
                        age = self.get_bdate(user_id)
                    elif len(bdate_list) == 3:
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
                            return age
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def get_city(self, user_id):
        try:
            city_dict = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'fields': 'city', 'v': '5.131'})
            for i in city_dict:
                for key, value in i.items():
                    city = i.get('city')
                    return city
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    # def get_dating_user(self, user_id):
    #     offset += 30
    #     self.get_daiting_user(self, user_id, offset=offset)

    def get_dating_users(self, user_id, offset = 75):
        global dating_dict
        try:
            dict_user_info = self.vk2.method('users.get', {'access_token': user_token, 'user_ids': user_id, 'fields': 'bdate, city, sex, relation', 'v': '5.131'})
            for i in dict_user_info:
                for key, value in i.items():
                    bdate = i.get('bdate')
                    city = i.get('city')
                    if (bdate is None and city is None) or (request == 'нет'):
                        data = self.get_user_data(user_id)
                        daiting_user = self.vk2.method('users.search',
                                                       {'access_token': user_token, 'sex': self.get_dating_sex(user_id),
                                                        'relation': 6, 'age_from': data['age_from'],
                                                        'age_to': data['age_to'], 'city': data['city'], 'friend_status': 0, 'has_photo': 1,
                                                        'offset': offset, 'fields': 'bdate, sex, city, relation', 'count': 30,
                                                        'v': '5.131'})
                        print(daiting_user)
                    else:
                        daiting_user = self.vk2.method('users.search',
                                                       {'access_token': user_token, 'sex': self.get_dating_sex(user_id),
                                                        'relation': 6, 'age_from': self.get_age(user_id) - 5,
                                                        'age_to': self.get_age(user_id) + 5, 'friend_status': 0,
                                                        'has_photo': 1,
                                                        'offset': offset, 'fields': 'bdate, sex, city, relation',
                                                        'count': 30,
                                                        'v': '5.131'})
                    du_list = daiting_user['items']
                    for i in du_list:
                        for key, value in i.items():
                            global vk_id, first_name, last_name
                            vk_id = i.get('id')
                            first_name = i.get('first_name')
                            last_name = i.get('last_name')
                            is_closed = i.get('is_closed')
                            bdate = i.get('bdate')
                            city = i.get('city')
                            if city == self.get_city(user_id) and is_closed == False:
                                dating_dict = {'vk_id': vk_id, 'first_name': first_name, 'last_name': last_name,
                                               'city': str(city.get('title')), 'bdate': bdate}
                                dating_list = (vk_id, first_name, last_name)
                                return dating_list
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def get_dating_user(self, user_id):
        global duser_id
        try:
            dating_list = self.get_dating_users(user_id)
            duser_id = dating_list[0]
            # user_list = self.get_user_info(user_id)
            # user = user_list[0]
            # print(user)
            # drop_users()
            create_db()
            create_users()
            select_users()
            select_duser_ids()
            print(select_duser_ids())
            # check_users(duser_id)
            # db_dusers_list = heck_users(duser_id)
            # for i in db_dusers_list:
            #     if i is None or i != duser_id:
            #         insert_users(dating_dict['vk_id'], dating_dict['first_name'], dating_dict['last_name'])
            #         photos_list = self.get_photos(duser_id)
            #         return self.send_some_msg(user_id, f'{dating_list[1]} {dating_list[2]}', photos_list)
            #     else:
            #         self.next(user_id)
            # insert_users(dating_dict['vk_id'], dating_dict['first_name'], dating_dict['last_name'])
            # photos_list = self.get_photos(duser_id)
            # return self.send_some_msg(user_id, f"{dating_dict['first_name']} {dating_dict['last_name']} {dating_dict['city']}", photos_list)
            # for i in db_dusers_list:
            #     if i is None or i != duser_id:
            #         insert_users(dating_dict['vk_id'], dating_dict['first_name'], dating_dict['last_name'])
            #         photos_list = self.get_photos(duser_id)
            #         return self.send_some_msg(user_id, f'{dating_list[1]} {dating_list[2]}', photos_list)
            #     else:
            #         self.next(user_id)
        # drop_users()
        # create_db()
        # create_users()
        # select_users()
        # return self.send_photos(user_id, f'photo{duser_id}_{photo1, photo2, photo3}')
        # return self.send_some_msg(user_id, f'{dating_list[1]} {dating_list[2]}', self.send_photos(user_id, photo{duser_id}_{photos_list}))

        # db_dusers = select_users()
        #     for i in db_dusers:
        #         for value in i.items():
        #             if duser_id == i.items[0]:
        #                 self.next(user_id)
        #     # items = [v[0] for v in db_dusers]
        #     # if duser_id in items:
        #     #     self.next(user_id)
        #     else:
        #     insert_users(dating_dict['vk_id'], dating_dict['first_name'], dating_dict['last_name'])
        #     return self.send_some_msg(user_id, f'{dating_list[1]} {dating_list[2]} {photos}')
            # return self.send_photos(user_id, f'{dating_list[1]} {dating_list[2]}', {photos[0]})
            # return self.send_photos(user_id, f'{dating_list[1]} {dating_list[2]}', {duser_id}_{self.get_photos(duser_id)})
            # return f"{self.send_some_msg(user_id, f'{dating_list[1]} {dating_list[2]}')} {self.send_photos(user_id, photos)}"
        except KeyError:
            return
        # else:
        #     self.next(user_id)

    # if __name__ == '__main__':
    #     print('вход bot.py')

    def get_photos(self, duser_id):
        try:
            photos = self.vk2.method('photos.get', {'access_token': user_token, 'album_id': 'profile', 'owner_id': duser_id, 'extended': 1, 'count': 3,  'v': '5.131'})
            photos_list = photos['items']
            # pprint(photos_list)
        except KeyError:
            return

        sorted_photos = sorted(photos_list, key=lambda x: x['likes']['count'], reverse=True)[:3]
        new_list = []
        for item in sorted_photos:
            photo_id = item.get('id')
            owner_id = item.get('owner_id')
            new_list.append(f'photo{owner_id}_{photo_id}')

        return ','.join(new_list)

    def hi(self, user_id):
        try:
            VkBot.send_some_msg(user_id, f'Привет, {VkBot.get_user_name(user_id)}! Если хочешь подобрать пару - набери "начать поиск"')
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def yes(self, user_id):
        try:
            VkBot.send_some_msg(user_id, f'{VkBot.get_dating_user(user_id)}')
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def no(self, user_id):
        try:
            VkBot.send_some_msg(user_id, f'{VkBot.get_user_data(user_id)}')
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def who(self, user_id):
        try:
            VkBot.send_some_msg(user_id, f'Твои данные: {VkBot.get_user_info(user_id)}')
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def next(self, user_id):
        try:
            VkBot.get_dating_user(user_id)
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def unclear(self, user_id):
        try:
            VkBot.send_some_msg(user_id, f'{self.get_user_name(user_id)}, твое сообщение мне не понятно, набери новое, пожалуйста.')
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')

    def bye(self, user_id):
        try:
            VkBot.send_some_msg(user_id, f'Пока, {VkBot.get_user_name(user_id)}! До новых встреч!')
        except KeyError:
            self.send_some_msg(user_id, 'Ошибка')


VkBot = VkBot()


for event in VkBot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        if request == 'привет':
            VkBot.hi(user_id)
        elif request == 'начать поиск':
            VkBot.get_daiting_user_info(user_id)
        elif request == 'да':
            VkBot.yes(user_id)
        elif request == 'нет':
            VkBot.no(user_id)
        elif request == 'кто я':
            VkBot.who(user_id)
        elif request == 'пока':
            VkBot.bye(user_id)
        elif request == 'еще':
            VkBot.next(user_id)
        else:
            VkBot.unclear(user_id)
