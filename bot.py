import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from vk_api.utils import get_random_id
from database import create_db, create_users, select_users, insert_users, drop_users, check_users
from config import group_token, user_token
from core import VkTools
import pprint
from datetime import datetime


class BotInterface:
    def __init__(self, group_token, user_token):
        self.interface = vk_api.VkApi(token=group_token)
        self.api = VkTools(user_token)
        self.params = {}
        self.users = {}
        self.offset = 0

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )
    def db(self, user_id):
        # drop_users
        create_db()
        create_users()
        select_users()

    def hi(self, user_id):
        self.params = self.api.get_profile_info(user_id)
        self.db(user_id)
        self.message_send(user_id,
                          f'''Привет, {self.params["name"]}! Набери команду:
                          поиск - начать поиск пары
                          справка - вызов списка команд
                          ''')

    def search_dating_user(self, user_id):
        try:
            self.message_send(user_id, f'{self.params["name"]}, идет поиск ...')
        except KeyError as e:
            users = []
            print(f'error = {e}')
            return self.message_send(user_id, 'Начни со слова привет')

        if self.users:
            user = self.users.pop()
            checkes_users = check_users(user['vk_id'])
            check = {str(user['vk_id']) for user['vk_id'] in checkes_users}
            if not check:
                photos_user = self.api.get_photos(user['vk_id'])
                self.message_send(user_id,
                                  f'Встречайте -  {user["first_name"]} {user["last_name"]}\n'
                                  f'ссылка: https://vk.com/id{user["vk_id"]}\n'
                                  f'написать https://vk.com/im?sel={user["vk_id"]}',
                                  photos_user
                                  )
                insert_users(user['vk_id'], user['first_name'], user['last_name'])
                print(user['vk_id'], user['first_name'], user['last_name'])

        else:
            self.users = self.api.serch_users(self.params, self.offset)
            user = self.users.pop()
            self.offset += 200

            # проверка бд
            checkes_users = check_users(user['vk_id'])
            check = {str(user['vk_id']) for user['vk_id'] in checkes_users}
            if not check:
                photos_user = self.api.get_photos(user['vk_id'])

                self.message_send(user_id,
                                  f'Встречайте -  {user["first_name"]} {user["last_name"]}\n '
                                  f'ссылка: https://vk.com/id{user["vk_id"]}\n'
                                  f'написать https://vk.com/im?sel={user["vk_id"]}',
                                  photos_user
                                  )

                # добавление в бд
                insert_users(user['vk_id'], user['first_name'], user['last_name'])
                print(user['vk_id'], user['first_name'], user['last_name'])
            else:
                print('User already in database')

    def next(self, user_id):
        self.search_dating_user(user_id)

    def help(self, user_id):
        self.message_send(user_id,
                          f'''Список команд:
                          справка - вызов списка команд
                          поиск - начать поиск пары
                          еще - показать следующую пару
                          кто я - вызов информации о себе
                          пока - завершить поиск
                          ''')

    def get_user_name(self, user_id):
        self.message_send(user_id, 'Введите ваше имя: ')
        for event in self.event_handler():
            name = event.text
        return name


    def get_user_bdate(self, user_id):
        self.message_send(user_id, 'Введите свою дату рождения в формате дд.мм.гггг: ')
        for event in self.event_handler():
            bdate = event.text
        return bdate

    def get_user_sex(self, user_id):
        self.message_send(user_id, 'Ваш пол (м/ж): ')
        for event in self.event_handler():
            sex = event.text
        return sex

    def get_user_city(self, user_id):
        self.message_send(user_id, 'Ваш пол (м/ж): ')
        for event in self.event_handler():
            city = event.text
        return city

    def user_name(self, user_id):
        name = self.params["name"]
        if name == None:
            name = self.get_user_name(user_id)
            return name
        else:
            return name

    def user_bdate(self, user_id):
        bdate = self.params["bdate"]
        if bdate == None:
            bdate = self.get_user_bdate(user_id)
            return bdate
        else:
            return bdate

    def user_sex(self, user_id):
        sex = self.params["sex"]
        if sex == None:
            sex = self.get_user_sex(user_id)
            return sex
        else:
            return sex

    def user_city(self, user_id):
        city = self.params["city"]
        if city == None:
            city= self.get_user_city(user_id)
            return city
        else:
            return city

    def who(self, user_id):
        try:
            self.message_send(user_id, f'''Твои данные: {self.user_name(user_id)}
                                        дата рождения: {self.params["bdate"]}
                                        пол: {self.user_sex(user_id)}
                                        город: {self.user_city(user_id)}
                            `            ''')

        except KeyError as e:
            users = []
            print(f'error = {e}')
            return self.message_send(user_id, 'Начни со слова привет')

    def bye(self, user_id):
        self.message_send(user_id, f'Пока! До новых встреч!')

    def unclear(self, user_id):
        self.message_send(user_id, f'Твое сообщение не понятно, набери новое, пожалуйста.\n Например, справка')

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()
                user_id = str(event.user_id)

                if command == 'привет':
                    self.hi(user_id)
                elif command == 'справка':
                    self.help(user_id)
                elif command == 'поиск':
                    self.search_dating_user(user_id)
                elif command == 'кто я':
                    self.who(user_id)
                elif command == 'еще':
                    self.next(user_id)
                elif command == 'пока':
                    self.bye(user_id)
                else:
                    self.unclear(user_id)

if __name__ == '__main__':
    bot = BotInterface(group_token, user_token)
    bot.event_handler()
    print('вход bot.py')
