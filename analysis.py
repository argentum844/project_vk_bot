import map_of_toponym


class Analysis:
    def __init__(self, text):
        self.text = text.lower()
        self.greeting = 'привет здравствуй здорово прив hi hello хай'.split()
        self.commands = ['Карта <название> <тип: гибрид, схема, спутник> \n(пример правильной команды: \"Карта Москва гибрид\")']
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
                res += i + '\n'
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
