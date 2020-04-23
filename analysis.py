import map_of_toponym
from admins import ADMINS, GOD
import map_of_organization
from db_session import DataBase
import speaker


class Analysis:
    def __init__(self, text, user_id):
        self.user_id = str(user_id)
        self.db = DataBase(text, user_id)
        self.db.insert_request()
        self.text = text.lower()
        self.greeting = 'привет здравствуй здорово прив hi hello хай'.split()
        self.commands = ['Карта <название> <тип: гибрид, схема, спутник> \n(пример правильной команды: Карта Москва гибрид)',
                         'Искать <организация> <тип: гибрид, схема, спутник> \n(пример правильной команды: искать аптеки в мичуринске гибрид)',
                         'Пробки <населенный пункт> <тип: гибрид, схема, спутник> \n(пример правильной команды: Пробки Москва гибрид)',
                         'Мои запросы', 'Очистить историю']
        if self.user_id in ADMINS:
            self.commands.append('Все запросы')
        if self.user_id in GOD:
            self.commands.append("Добавить админа")
            self.commands.append("Удалить админа")
            self.commands.append("Админы")
        self.result = self.analys()

    def get_result(self):
        return self.result

    def analys(self):
        result = ''
        priv = self.is_hello()
        com = self.is_commands()
        com1 = self.is_first_command()
        com2 = self.is_second_command()
        com3 = self.is_third_command()
        com4 = self.is_fourth_command()
        com5 = self.is_fifth_command()
        com6 = self.is_sixth_command()
        add_admin = self.add_admin()
        remove_admin = self.remove_admin()
        adm = self.all_admins()
        if priv:
            result = priv
        elif com:
            result = com
        elif com1:
            result = com1
        elif com2:
            result = com2
        elif com3:
            result = com3
        elif com4:
            result = com4
        elif com5:
            result = com5
        elif com6:
            result = com6
        elif add_admin:
            result = add_admin
        elif remove_admin:
            result = remove_admin
        elif adm:
            result = adm
        else:
            result = speaker.Speaker(self.text).get_result()
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
            if self.user_id not in ADMINS:
                return "Недостаточный уровень допуска"
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

    def is_fifth_command(self):
        if self.text.startswith('искать'):
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
                return 'Вы не ввели название организации'
            return map_of_organization.MapOfOrganization(toponym, type_map).get_result()
        return False

    def is_sixth_command(self):
        if self.text.startswith('пробки'):
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
            return map_of_toponym.MapOfToponym(toponym, type_map, True).get_result()
        return False

    def add_admin(self):
        if self.text.startswith("добавить админа"):
            if self.user_id in GOD:
                a = self.text.split()
                if len(a) < 3:
                    return "Вы не ввели id админа"
                user_id = a
                ADMINS.add(user_id)
                f = open('admins.txt', 'w')
                f.write('\n'.join([x for x in ADMINS]))
                f.close()
                return f"Админ добавлен: {user_id}"
            else:
                return "Недостаточный уровень допуска"
        return False

    def remove_admin(self):
        if self.text.startswith("удалить админа"):
            if self.user_id in GOD:
                a = self.text.split()
                if len(a) < 3:
                    return "Вы не ввели id админа"
                user_id = a
                if user_id not in ADMINS:
                    return "Пользователь не является админом"
                ADMINS.remove(user_id)
                f = open('admins.txt', 'w')
                f.write('\n'.join([x for x in ADMINS]))
                f.close()
                return f"Админ удален: {user_id}"
            else:
                return "Недостаточный уровень допуска"
        return False

    def all_admins(self):
        if self.text == "админы":
            if self.user_id in GOD:
                return '\n'.join(ADMINS)
            else:
                return "Недостаточный уровень допуска"
        return False
