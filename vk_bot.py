import bs4

from bot_commands import *
from application.db.bot_dictionary import first_word, last_word

candidate_values = {
            'sex': 0,
            'age_from': 0,
            'age_to': 0,
            'city': 0,
            'status': 0,
            'switch': 0
        }
candidate = {'sex': '',
             'age_from': 0,
             'age_to': 0,
             'city': '',
             'status': ''}


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
            candidate_values['switch'] = 1  #
            return f'Здравствуйте {self.username}! Начинаем поиск.\nВыберете пол (М / Ж):'

        elif candidate_values['switch'] == 1 and (message.lower() not in 'мж'):
            return 'Необходимо ввксти букву "м"  или  "ж"'

        elif message.lower() == 'инфо':
            return f'Привет {self.username}\n{Search.info.__doc__}'

        elif candidate_values['switch'] == 1 and message.lower() == 'м':
            candidate_values['switch'] = 2
            candidate_values['sex'] = 2
            candidate['sex'] = 'Мужчина'
            return 'Введите возраст  От - До  (через пробел)'

        elif candidate_values['switch'] == 1 and message.lower() == 'ж':
            candidate_values['switch'] = 2
            candidate_values['sex'] = 1
            candidate['sex'] = 'Женщина'
            return 'Введите возраст  От - До  (через пробел)'

        elif candidate_values['switch'] == 2 and len(message.split()) == 2:
            result = message.split()
            if result[0].isdigit() and result[-1].isdigit():
                candidate_values['age_from'] = int(result[0])
                candidate['age_from'] = result[0]
                candidate_values['age_to'] = int(result[-1])
                candidate['age_to'] = result[-1]
                candidate_values['switch'] = 3

                return f'Введите семейное положение.\n{Search.status()}'

            else:
                return 'Ошибка ввода, попробуйте ещё раз'

        elif candidate_values['switch'] == 2 and message.isalpha():
            return 'Необходимо ввести ТОЛЬКО циифры через пробел'

        elif candidate_values['switch'] == 2 and message.isdigit():
            return 'Необходимо ввести только циифры ЧЕРЕЗ ПРОБЕЛ'

        elif candidate_values['switch'] == 3 and message not in '12345678':
            return 'Допустимы только цифры от 1 до 8'

        elif candidate_values['switch'] == 3 and message.isdigit():
            candidate_values['status'] = int(message)
            candidate['status'] = Search.add_status(message)
            candidate_values['switch'] = 4
            return 'Введите название города'

        elif candidate_values['switch'] == 4 and message.isalpha():
            candidate_values['city'] = Search().city_search(message.lower())
            candidate['city'] = message
            candidate_values['switch'] = 5
            return f'Проверьте данные:\n{candidate["sex"]} от {candidate["age_from"]} до {candidate["age_to"]} ' \
                   f'{candidate["status"]}\nИз города {candidate["city"].capitalize()}' \
                   f'\nДля запуска поиска введите "старт"\nДля отмены введите "стоп"\nДля корректировки введите "сброс"'

        elif candidate_values['switch'] == 4 and message.isdigit():
            return 'В названии не должно быть цифры'

        elif candidate_values['switch'] == 5 and message.lower() == 'старт':
            Search().get_search(candidate_values)
            VkSaver().photo_search()
            print(' итоговый запрос: ', candidate_values)
            return 'Начали поиск'

        elif candidate_values['switch'] == 5 and message.lower() == 'сброс':
            candidate_values['switch'] = 1
            return 'Повторите ввод данных:\nВыберете пол (М / Ж):'

        elif message.lower() in last_word:
            return f"Пока-пока, {self.username}!"

        else:
            return Search.wrong_word()


if __name__ == '__main__':
    print("hi, i'm VkBot")
