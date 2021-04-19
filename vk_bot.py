import bs4

from bot_commands import *
from application.db.bot_dictionary import first_word, last_word

candidate_values = {
            'sex': 0,
            'age_from': 0,
            'age_to': 0,
            'city': 0,
            'status': 0
        }
candidate = {'sex': '',
             'age_from': 0,
             'age_to': 0,
             'city': '',
             'status': ''}

params = {
    'start_dialog': False,
    'input_age': False,
    'input_status': False,
    'input_city': False,
    'ready': False,
    'search_completed': False
    }
cut_candidates_dict = {}


class VkBot:

    def __init__(self, user_id):
        self.username = self._get_user_name_from_vk_id(user_id)

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    def new_message(self, message):
        """
        Общение с ботом
        :param message: str
        :return: str
        """
        if message.lower() in first_word:
            params['start_dialog'] = True
            return f'Здравствуйте {self.username}! Начинаем поиск.\nВыберете пол (М / Ж):'

        elif params['start_dialog'] and (message.lower() not in 'мж'):
            return 'Необходимо ввести букву "м"  или  "ж"'

        elif message.lower() == 'инфо':
            return f'Привет {self.username}\n{Search.info.__doc__}'

        elif params['start_dialog'] and message.lower() == 'м':
            params['input_age'] = True
            params['start_dialog'] = False
            candidate_values['sex'] = 2
            candidate['sex'] = 'Мужчина'
            return 'Введите возраст  От - До  (через пробел)'

        elif params['start_dialog'] and message.lower() == 'ж':
            params['input_age'] = True
            params['start_dialog'] = False
            candidate_values['sex'] = 1
            candidate['sex'] = 'Женщина'
            return 'Введите возраст  От - До  (через пробел)'

        elif params['input_age'] and message.isalpha():
            return 'Необходимо ввести ТОЛЬКО циифры через пробел'

        elif params['input_age'] and message.isdigit():
            return 'Необходимо ввести две циифры ЧЕРЕЗ ПРОБЕЛ'

        elif params['input_age'] and len(message.split()) == 2:
            result = message.split()
            if result[0].isdigit() and result[-1].isdigit():
                candidate_values['age_from'] = int(result[0])
                candidate['age_from'] = result[0]
                candidate_values['age_to'] = int(result[-1])
                candidate['age_to'] = result[-1]
                params['input_status'] = True
                params['input_age'] = False
                return f'Введите семейное положение.\n{Search.status()}'

            else:
                return 'Ошибка ввода, попробуйте ещё раз'

        elif params['input_status'] and message not in '12345678':
            return 'Допустимы только цифры от 1 до 8'

        elif params['input_status'] and message in '12345678':
            candidate_values['status'] = int(message)
            candidate['status'] = Search.add_status(message)
            params['input_city'] = True
            params['input_status'] = False
            return 'Введите название города'

        elif params['input_city'] and message.isalpha():
            city_title = Search().city_search(message.lower())
            if type(city_title) == int:
                candidate_values['city'] = city_title
                candidate['city'] = message
                params['ready'] = True
                params['input_city'] = False
                return f'Проверьте данные:\n{candidate["sex"]} от {candidate["age_from"]} до {candidate["age_to"]} ' \
                       f'{candidate["status"]}\nИз города {candidate["city"].capitalize()}' \
                       f'\nДля запуска поиска введите "старт"\nДля отмены введите "стоп"\nДля корректировки введите "сброс"'
            else:
                return city_title

        elif params['input_city'] and message.isdigit():
            return 'В названии не должно быть цифры'

        elif params['ready'] and message.lower() == 'старт':
            params['ready'] = False
            params['search_completed'] = True
            Search().get_search(candidate_values)
            cut_candidate = VkSaver().photo_search()
            for key, item in cut_candidate.items():
                cut_candidates_dict[key] = item
            return 'Поиск завершен.\n1 - просмотр результатов'

        elif params['ready'] and message.lower() == 'сброс':
            params['start_dialog'] = True
            return 'Повторите ввод данных:\nВыберете пол (М / Ж):'

        elif params['search_completed'] and message == '1':
            print(cut_candidates_dict)
            return cut_candidates_dict

        elif message.lower() in last_word:
            return f"Пока-пока, {self.username}!"

        else:
            return Search.wrong_word()


if __name__ == '__main__':
    print("hi, i'm VkBot")
