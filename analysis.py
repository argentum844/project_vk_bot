import map_of_toponym


class Analysis:
    def __init__(self, text):
        self.text = text.lower()
        self.greeting = 'привет здравствуй здорово прив hi hello хай'.split()
        self.commands = ['Карта населенного пункта: <название> <тип: гибрид, схема, спутник> \n(пример правильной команды: \"Карта населенного пункта: Москва; гибрид\")']
        self.result = self.analys()

    def get_result(self):
        return self.result

    def analys(self):
        if any([x in self.text for x in self.greeting]):
            return "привет"
        if "команды" in self.text:
            res = ''
            for i in self.commands:
                res += i + '\n'
            return res
        if 'карта населенного пункта' in self.text:
            if ':' not in self.text or '<' in self.text or ">" in self.text:
                return "Неправильный синтаксис команды. Пример правильной команды: \"Карта населенного пункта: Москва; гибрид\""
            toponym = self.text.split(': ')[1].split('; ')
            if len(toponym) == 0 or len(toponym) > 2:
                return "Неправильный синтаксис команды. Пример правильной команды: \"Карта населенного пункта: Москва; гибрид\""
            if len(toponym) == 2:
                if toponym[1] == 'схема':
                    toponym[1] = 'scheme'
                elif toponym[1] == 'гибрид':
                    toponym[1] = 'hybrid'
                elif toponym[1] == 'спутник':
                    toponym[1] == 'satellite'
                else:
                    return "Неправильный синтаксис команды. Пример правильной команды: \"Карта населенного пункта: Москва; гибрид\""
                return map_of_toponym.MapOfToponym(toponym[0], toponym[1]).get_result()
            else:
                return map_of_toponym.MapOfToponym(toponym[0]).get_result()
        return "чтобы посмотреть возможные команды, напиши слово \"Команды\""
