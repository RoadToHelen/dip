import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from vk_api.utils import get_random_id
from database import DBTools
from config import group_token, user_token
from core import VkTools


class BotInterface:
    def __init__(self, group_token, user_token):
        self.interface = vk_api.VkApi(token=group_token)
        self.api = VkTools(user_token)
        self.db = DBTools
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
        #self.db.drop_users
        self.db.create_db()
        self.db.create_users()
        self.db.select_users()

    def hi(self, user_id):
        self.params = self.api.get_profile_info(user_id)
        self.message_send(user_id,
                          f'''Привет, {self.params["name"]}! Набери команду:
                          поиск - начать поиск пары
                          справка - вызов списка команд
                          ''')
        self.db(user_id)

    def search_dating_user(self, user_id):
        try:
            self.message_send(user_id, f'{self.params["name"]}, идет поиск ...')
        except KeyError as e:
            users = []
            print(f'error = {e}')
            return self.message_send(user_id, 'Начни со слова привет')

        if self.users:
            user = self.users.pop()
            checkes_users = self.db.check_users(user['vk_id'])
            check = {str(user['vk_id']) for user['vk_id'] in checkes_users}
            if not check:
                photos_user = self.api.get_photos(user['vk_id'])
                self.message_send(user_id,
                                  f'Встречайте -  {user["first_name"]} {user["last_name"]}\n'
                                  f'ссылка: https://vk.com/id{user["vk_id"]}\n'
                                  f'написать https://vk.com/im?sel={user["vk_id"]}',
                                  photos_user
                                  )
                self.db.insert_users(user['vk_id'], user['first_name'], user['last_name'])
                print(user['vk_id'], user['first_name'], user['last_name'])

        else:
            self.users = self.api.serch_users(self.params, self.offset)
            user = self.users.pop()
            self.offset += 0

            # проверка бд
            checkes_users = self.db.check_users(user['vk_id'])
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
                self.db.insert_users(user['vk_id'], user['first_name'], user['last_name'])
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

    def who(self, user_id):
        try:
            self.message_send(user_id, f'Твои данные: {self.params["name"]}')
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
