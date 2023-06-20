import vk_api
from datetime import datetime
from config import user_token
from vk_api.exceptions import ApiError
from datetime import datetime
from pprint import pprint

class VkTools():
    def __init__(self, user_token):
        self.api = vk_api.VkApi(token=user_token)

    def get_profile_info(self, user_id):
        try:
            info, = self.api.method('users.get',
                                    {'user_id': user_id,
                                     'fields': 'city,bdate,sex,relation,home_town'
                                     }
                                    )
        except ApiError as e:
            info = {}
            print(f'error = {e}')

        user_info = {'name': info['first_name'] + ' ' + info['last_name'],
                     'id': info['id'],
                     'bdate': info['bdate'] if 'bdate' in info else None,
                     'home_town': info['home_town'],
                     'sex': info['sex'],
                     'city': info['city']['id']
                     }
        return user_info

    def serch_users(self, params):

        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        curent_year = datetime.now().year
        user_year = int(params['bdate'].split('.')[2])
        age = curent_year - user_year
        age_from = age - 5
        age_to = age + 5

        try:
            users = self.api.method('users.search',
                                    {'count': 30,
                                     'offset': 0,
                                     'age_from': age_from,
                                     'age_to': age_to,
                                     'sex': sex,
                                     'city': city,
                                     'status': 6,
                                     'is_closed': False
                                     }
                                    )
        except ApiError as e:
            users = []
            print(f'error = {e}')

        pprint(users)

        try:
            users = users['items']
        except KeyError:
            return []

        res = []

        for user in users:
            if user['is_closed'] == False:
                res.append({'id': user['id'],
                            'name': user['first_name'] + ' ' + user['last_name']
                            }
                           )

        return res

    def get_photos(self, user_id):
        photos = self.api.method('photos.get',
                                 {'user_id': user_id,
                                  'album_id': 'profile',
                                  'extended': 1,
                                  'count': 3,
                                  'v': '5.131'
                                  }
                                 )
        try:
            photos_list = photos['items']
        except KeyError:
            return []

        sorted_photos = sorted(photos_list, key=lambda x: x['likes']['count'], reverse=True)[:3]
        new_list = []
        for item in sorted_photos:
            photo_id = item.get('id')
            owner_id = item.get('owner_id')
            new_list.append(f'photo{owner_id}_{photo_id}')

        return ','.join(new_list)


# if __name__ == '__main__':
#     bot = VkTools(user_token)
#     params = bot.get_profile_info(789657038)
#     users = bot.serch_users(params)
#     print(bot.get_photos(users[2]['id']))
