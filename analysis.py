class Analysis:
    def __init__(self, text):
        self.text = text.lower()
        self.greeting = 'привет здравствуй здорово прив hi hello хай'.split()
        self.commands = 'Карта места, Карта населенного пункта, Что нибудь ещё'.split(', ')
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
        return "чтобы посмотреть возможные команды, напиши слово \"Команды\""
