import requests

from application.db.database import get_people_information, get_most_of_liked_photos, get_owner_id_list
from application.db.user_information import user_token
import time


links_dict = {}


class Search:

    def __init__(self):
        self.url = 'http://api.vk.com/method/'
        self.user_token = user_token
        self.params = {
                       'v': '5.89',
                       'country_id': '1'
                       }

    @staticmethod
    def wrong_word():
        return 'Вас приветствует Bot VKinder.' \
               'Для получения справки введите "инфо"\n Для начала работы напишите "Привет"'

    @staticmethod
    def status():
        return '1 - не женат (не замужем)\n2 - встречается\n3 - помолвлен(-а)\n4 - женат (замужем)\n5 - всё сложно\n' \
               '6 - в активном поиске\n7 - влюблен(-а)\n8 - в гражданском браке'

    @staticmethod
    def add_status(text):
        owner_status = {
            '1': 'женат (не замужем)',
            '2': 'встречается',
            '3': 'помолвлен(-а)',
            '4': 'женат (замужем)',
            '5': 'всё сложно',
            '6': 'в активном поиске',
            '7': 'влюблен(-а)',
            '8': 'в гражданском браке',
          }
        return owner_status[text]

    @staticmethod
    def info():
        """
        Приложение VKinder.
        Поиск людей по заданным параметрам в соцеальной сети "Вконтакте".

        Вводите данные для поискового запроса:
        - пол
        - возраст
        - город
        - семейное положение

        Далее программа просматривает страницы, подходящие под параметры, находит для просмотра TOP-3 фотографии профиля
        и возвращает ссылку на страницу пользователя.
        Вам будет предложено оценить получившиеся результаты и внести кандидата в "Белый" или "Чёрный" список.
        """
        return True

    def get_search(self, candidate_info: dict):
        """
        Поиск людей по параметрам
        :param candidate_info: dict
        :return: str
        """
        search_params = {
            'access_token': self.user_token,
            'sex': candidate_info['sex'],
            'status': candidate_info['status'],
            'age_from': candidate_info['age_from'],
            'age_to': candidate_info['age_to'],
            'city': candidate_info['city'],
            'sort': 0,
            'count': 500,
            'has_photo': 1
            }
        peoples = requests.get(self.url + 'users.search', params={
            **self.params, **search_params}).json()['response']['items']
        owner_id_list = get_owner_id_list()
        for person in peoples:
            if person['is_closed'] is False:
                if str(person['id']) not in owner_id_list:
                    link = [person['first_name'] + ' ' + person['last_name'], person['id']]
                    links_dict[person['id']] = link

        return 'запрос выполнен'

    def city_search(self, city_title):
        """
        Поиск идентификатора города
        :param city_title: str
        :return: int
        """
        search_params = {
                  'access_token': self.user_token,
                  'q': city_title.capitalize(),
                  'count': '10'
                  }
        try:
            city_id = requests.get(self.url + 'database.getCities', params={
                **self.params, **search_params}).json()['response']['items'][0]['id']
            return city_id
        except IndexError:
            return 'ошибка, нет такого города\nВведите название города'


class VkSaver(Search):
    def __init__(self, owner_id=None):
        super(VkSaver, self).__init__()
        self.owner_id = owner_id
        self.photo_stock = {}
        self.candidates_dict = {}

    def get_photo(self, owner_id, album_id=None):
        """
        Получаем фото профиля по id
        :param owner_id: int
        :param album_id: str
        :return: dict
        """
        if album_id is None:
            album_id = 'profile'
        gp_params = {
            'access_token': self.user_token,
            'user_id': owner_id,
            'extended': 1,
            'photo_sizes': 1,
            'album_id': album_id
        }
        response = requests.get(self.url + 'photos.get', params={**self.params, **gp_params}).json()
        time.sleep(0.3)
        count_photos = response['response']['count']
        if count_photos >= 3:
            for items in response['response']['items']:
                self.photo_stock[items['sizes'][-1]['url']] = items['likes']['count']
        else:
            pass
        sorted_tuple = sorted(self.photo_stock.items(), key=lambda x: x[1])
        limited_tuple = sorted_tuple[-3:]
        return limited_tuple

    def photo_search(self):
        """
        Поиск по списку полученных id
        :return: dict
        """
        print(links_dict)
        for owner_id in list(links_dict.values()):
            result = self.get_photo(owner_id[-1])
            self.photo_stock = {}
            if result:
                get_people_information(owner_id)
                get_most_of_liked_photos(owner_id[-1], result)
                self.candidates_dict[owner_id[-1]] = result
        links_dict.clear()
        return self.candidates_dict


if __name__ == '__main__':
    print('module')
