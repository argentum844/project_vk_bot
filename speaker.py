import random


class Speaker:
    def __init__(self, text):
        self.text = text
        self.result = self.analys()

    def get_result(self):
        return self.result

    def analys(self):
        if "как " in self.text and "дела" in self.text:
            variants = ['Отлично!', 'Так себе', 'Плохо', 'Хорошо']
            return random.choice(variants)

        if 'что ' in self.text and 'делаешь' in self.text:
            variants = ['Чай пью', 'В Mortal Combat рублюсь', 'Сплю (уже нет, "спасибо")',
                        'С тобой переписываюсь (да неужели О_о)', 'Строю теории заговора', 'Смотрю на котиков']
            return random.choice(variants)

        if "почему" in self.text:
            variants = ['Потому что', 'А тебе зачем это знать?', 'Не знаю']
            return random.choice(variants)

        if "зачем" in self.text or "для чего" in self.text:
            variants = ['так надо', 'чтобы ты спросил', 'Не знаю']
            return random.choice(variants)

        if "как " in self.text:
            variants = ['Как-то', 'А тебе зачем?']
            return random.choice(variants)
        
        return ''
