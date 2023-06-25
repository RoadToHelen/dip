import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from vk_api.utils import get_random_id
from database import create_db, create_users, select_users, insert_users, drop_users, check_users
from config import group_token, user_token
from core import VkTools


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
        create_db()
        create_users()
        select_users()

    def next_user(self, user_id):
        # user_id = event.user_id
        users = self.api.serch_users(self.params)
        user = users.pop()
        checkes_users = check_users(user['vk_id'])
        check = {str(user['vk_id']) for user['vk_id'] in checkes_users}
        if not check:
            photos_user = self.api.get_photos(user['vk_id'])

            self.message_send(user_id,
                              f'Встречайте -  {user["first_name"]} {user["last_name"]}',
                              photos_user
                              )

    # def hi(self, user_id):
    #     self.params = self.api.get_profile_info(user_id)
    #     self.message_send(user_id, f'Привет, {self.params["name"]}! Если хочешь подобрать пару - набери "поиск"')

    # def search(self, user_id):
    #     users = self.api.serch_users(self.params)
    #     user = users.pop()

    # def check_params(self, user_id):
    #     params = self.api.get_profile_info(user_id)
    #     for i in params:
    #         for 'name' == None:
    #             name = self.message_send(user_id, f'Ваше имя: ')

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()
                user_id = event.user_id

                if command == 'привет':
                    self.params = self.api.get_profile_info(user_id)
                    self.message_send(user_id,
                                      f'Привет, {self.params["name"]}! Если хочешь подобрать пару - набери "поиск"')
                elif command == 'поиск':
                    self.message_send(event.user_id, f'{self.params["name"]}, идет поиск ...')
                    self.db(event.user_id)

                    if self.users:
                        user = self.users.pop()
                        checkes_users = check_users(user['vk_id'])
                        check = {str(user['vk_id']) for user['vk_id'] in checkes_users}
                        if not check:
                            photos_user = self.api.get_photos(user['vk_id'])
                            self.message_send(event.user_id,
                                              f'Встречайте -  {user["first_name"]} {user["last_name"]} ',
                                              photos_user
                                              )
                            insert_users(user['vk_id'], user['first_name'], user['last_name'])
                            print(user['vk_id'], user['first_name'], user['last_name'])


                    else:
                        self.users = self.api.serch_users(self.params, self.offset)
                        user = self.users.pop()
                        self.offset += 30

                        # логика для проверки бд
                        checkes_users = check_users(user['vk_id'])
                        check = {str(user['vk_id']) for user['vk_id'] in checkes_users}
                        if not check:
                            photos_user = self.api.get_photos(user['vk_id'])

                            self.message_send(event.user_id,
                                              f'Встречайте -  {user["first_name"]} {user["last_name"]} ссылка: vk.com/{user["vk_id"]}',
                                              photos_user
                                              )

                            # здесь логика для добавленяи в бд
                            insert_users(user['vk_id'], user['first_name'],  user['last_name'])
                            print(user['vk_id'], user['first_name'],  user['last_name'])
                        else:
                            print('User already in database')

                elif command == 'пока':
                    self.message_send(event.user_id, f'До новых встреч!')
                else:
                    self.message_send(event.user_id, f'Твое сообщение мне не понятно, набери новое, пожалуйста.')

if __name__ == '__main__':
    bot = BotInterface(group_token, user_token)
    bot.event_handler()
