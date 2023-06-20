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
        self.params = None

    def message_send(self, user_id, message, attachment=None):
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )

    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()

                if command == 'привет':
                    self.params = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'Привет, {self.params["name"]}! Если хочешь подобрать пару - набери "поиск"')
                elif command == 'поиск':
                    users = self.api.serch_users(self.params)
                    user = users.pop()

                    # здесь логика для проверки бд
                    # create_db()
                    # create_users()
                    # select_users()
                    # checkes_users = check_users(user['id'])
                    # check = {str(dating_list[0]) for user['id'] in checkes_users}
                    # if not check:
                    photos_user = self.api.get_photos(user['id'])

                    self.message_send(event.user_id,
                                      f'Встречайте -  {user["name"]}',
                                      photos_user
                                      )
                    # здесь логика для добавленяи в бд
                    #insert_users(user['id'], dating_dict['first_name'], dating_dict['last_name'])

                elif command == 'пока':
                    self.message_send(event.user_id, f'до новых встреч!')
                else:
                    self.message_send(event.user_id, f'твое сообщение мне не понятно, набери новое, пожалуйста.')

if __name__ == '__main__':
    bot = BotInterface(group_token, user_token)
    bot.event_handler()
