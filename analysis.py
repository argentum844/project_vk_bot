import map_of_toponym
from db_session import DataBase


class Analysis:
    def __init__(self, text, user_id):
        self.db = DataBase(text, user_id)
        self.db.insert_request()
        self.text = text.lower()
        self.greeting = 'привет здравствуй здорово прив hi hello хай'.split()
        self.commands = ['Карта <название> <тип: гибрид, схема, спутник> \n(пример правильной команды: \"Карта Москва гибрид\")',
                         'Мои запросы', 'Все запросы', 'очистить историю']
        self.result = self.analys()

    def get_result(self):
        return self.result

    def analys(self):
        result = ''
        if self.is_hello():
            result = self.is_hello()
        elif self.is_commands():
            result = self.is_commands()
        elif self.is_first_command():
            result = self.is_first_command()
        elif self.is_second_command():
            result = self.is_second_command()
        elif self.is_third_command():
            result = self.is_third_command()
        elif self.is_fourth_command():
            result = self.is_fourth_command()
        if result == '':
            result = "чтобы посмотреть возможные команды, напиши слово \"Команды\""
        return result

    def is_hello(self):
        if any([x in self.text for x in self.greeting]):
            return "привет" + '\n'
        return False

    def is_commands(self):
        if "команд" in self.text:
            res = ''
            for i in self.commands:
                res += i + '\n\n'
            return res
        return False

    def is_first_command(self):
        if self.text.startswith('карта'):
            text = self.text.split()[1:]
            toponym = ''
            type_map = 'scheme'
            for i in text:
                if 'гибрид' in i:
                    type_map = 'hybrid'
                elif 'схема' in i:
                    type_map = 'scheme'
                elif 'спутник' in i:
                    type_map = 'satellite'
                else:
                    toponym += i + ' '
            if toponym == '':
                return 'Вы не ввели название населенного пункта'
            return map_of_toponym.MapOfToponym(toponym, type_map).get_result()
        return False

    def is_second_command(self):
        if "мои запросы" in self.text:
            res = '\n'.join([x[0] for x in self.db.get_requests(True)])
            if res == '':
                return 'что-то пошло не так'
            return res
        return False

    def is_third_command(self):
        if "все запросы" in self.text:
            res = '\n'.join([x[0] for x in self.db.get_requests(False)])
            if res == '':
                return 'что-то пошло не так'
            return res
        return False

    def is_fourth_command(self):
        if "очистить историю" in self.text:
            res = self.db.delete_history()
            if not res:
                return 'что-то пошло не так'
            else:
                return 'история очищена'
        return False
