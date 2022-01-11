'''Банкомат реализованый с помощью SQLite3
Так же добавлен пункт меню по выводу курса валют'''

import sqlite3
import os
import datetime as dt
import requests
import json

class BadOuth(Exception):
    def __init__(self, msg):
        self.msg = msg
class LoginIsBusy(Exception):
    def __init__(self, msg):
        self.msg = msg
class Problem(Exception):
    def __init__(self, msg):
        self.msg = msg


path = os.path.dirname(os.path.realpath(__file__)) + '/'
con = sqlite3.connect('ATM.db')
cur = con.cursor()

class ATM(object):
# доделать проверку при статре программы, если такие пользователи в базе есть то продолжить, если нет то создать их.
    def default_users(self):
        users = [
            ('user1', 'user1', False),
            ('user2', 'user2', False),
            ('admin', 'admin', True),
        ]
        for user in users:
            exists = cur.execute('''SELECT id FROM users WHERE username=?''', (user[0],)).fetchone()
            if not exists:
                cur.execute('INSERT INTO users (username, password, is_incasator) VALUES (?, ?, ?);', user)
                con.commit()
                user_id = cur.execute('''SELECT id FROM users WHERE username=?''', (user[0],)).fetchone()[0]
                cur.execute('INSERT INTO balance (user_id, amount) VALUES (?, ?);', (user_id, 0))
                con.commit()
        self.default_atm()

    def default_atm(self):
        nominals = [
            ('1000', 10),
            ('500', 10),
            ('200', 10),
            ('100', 10),
            ('50', 10),
            ('20', 10),
            ('10', 10)
        ]
        for nominal in nominals:
            cur.execute('INSERT INTO balance_atm (nominal, number) VALUES (?, ?)', nominal)
            con.commit()

    def create_table(self):
        # users
        cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id integer NOT NULL PRIMARY KEY,
        username text NOT NULL,
        password text NOT NULL,
        is_incasator bit DEFAULT false
    );
    ''')
        # balance
        cur.execute('''
    CREATE TABLE IF NOT EXISTS balance (
        user_id integer NOT NULL,
        amount float NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    ''')
        # balance_atm
        cur.execute('''
    CREATE TABLE IF NOT EXISTS balance_atm (
        nominal text NOT NULL,
        number integer NOT NULL DEFAULT 10
    );
    ''')
        # transactions
        cur.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        user text NOT NULL,
        date text NOT NULL,
        massage text NOT NULL,
        FOREIGN KEY (user) REFERENCES users (username)
    );
    ''')

    def registration(self):
        login = input('Придумайте и введите логин: ')
        password = input('Придумайте и введите пароль: ')
        user = (str(login), str(password))
        user_in_db = cur.execute('''SELECT username FROM users WHERE username=? AND password=?''', user).fetchall()
        if not user_in_db:
            cur.execute('INSERT INTO users (username, password) VALUES (?, ?);', user)
            con.commit()
            user_id = cur.execute('''SELECT id FROM users WHERE username=?''', (user[0],)).fetchone()[0]
            cur.execute('INSERT INTO balance (user_id, amount) VALUES (?, ?);', (user_id, 0))
            con.commit()
            print('--- User Created saccess. ---')
        else:
            print('--- Login in busy, please try again. ---')

    def autorization(self):
        count = 3
        for i in range(3):
            login = input('Введите ваш логин: ')
            password = input('Введите ваш пароль: ')
            user = (login, password)
            user_in_db = cur.execute('''SELECT username, password, is_incasator FROM users WHERE username=? AND password=?''', user).fetchone()
            if user_in_db:
                if user_in_db[2] == 1:
                    print('STATUS INCASATOR')
                else:
                    print('STATUS OK')
                return user_in_db
            else:
                count -= 1
                print(f'--- Логин или пароль не верный, попыток осталось {count} ---')
                continue
        raise BadOuth('Не верный логин или пароль!!!')

    def menu_start(self):
        self.create_table()
        self.default_users()
        while True:
            print('1 - для регистрации')
            print('2 - для авторизации')
            print('3 - для вывода текущего курса валют')
            print('4 - для выхода из программы')
            choice = input('Ваш выбор: ')
            if choice == '1':
                self.registration()
            elif choice == '2':
                login, password, incasation = self.autorization()
                if incasation:
                    self.menu_incasation()
                else:
                    self.menu_user(login)
            elif choice == '3':
                self.show_currency()
            elif choice == '4':
                exit()
            else:
                print('НЕТ ТАКОГО ВАРИАНТА.')

    # ниже блок инкасатора
    def menu_incasation(self):
        while True:
            print('1 - для вывода остатка средств в банкомате')
            print('2 - для добавления денег в банкомат')
            print('3 - для выхода')
            choice_inc = input('Ваш выбор: ')
            if choice_inc == '1':
                self.show_balance_atm()
            elif choice_inc == '2':
                self.add_balance_atm()
            elif choice_inc == '3':
                exit()
            else:
                print('Таких вариантов нет!')
                continue

    def show_balance_atm(self):
        nominals = cur.execute('SELECT * FROM balance_atm').fetchall()
        nominal = {}
        for i in nominals:
            nominal[i[0]] = i[1]

        print('Номинал:')
        for k, v in nominal.items():
            print(f'{k.ljust(6)}{str(v).rjust(5)}')
        print('*' * 50)

    def add_balance_atm(self):
        nominals = cur.execute('SELECT * FROM balance_atm').fetchall()
        nominal = {}
        for i in nominals:
            nominal[i[0]] = i[1]
        while True:
            addition = input('Введите номинал и количество (пример: 1000, 10) или введите exit: ')  # ['1000', '10']
            if addition == 'exit':
                 break
            addition = addition.split(', ') #['1000', '10']
            if addition[0] not in ['1000', '500', '200', '100', '50', '20', '10']:
                print('НЕТ ТАКОГО НОМИНАЛА.')
                continue
            nominal[addition[0]] += abs(int(addition[1]))
            cur.execute('UPDATE balance_atm SET number=? WHERE nominal=?', (nominal[addition[0]], addition[0]))
            con.commit()


    # Ниже код для работы с пользователем.
    def menu_user(self, login):
        while True:
            print('1 - для просмотра баланса.')
            print('2 - для пополнения баланса.')
            print('3 - для снятия средств с баланса.')
            print('4 - для возвращения в предыдущее меню.')
            print('5 - для выхода из программы.')
            choice = input('Ваш выбор: ')
            if choice == '1':
                self.show_balance(login)
            elif choice == '2':
                self.add_balance(login)
            elif choice == '3':
                self.withdraw_balance(login)
            elif choice == '4':
                break
            elif choice == '5':
                print('Спасибо что воспользовались нашим банкоматом!')
                exit()
            else:
                print('НЕТ ТАКОГО ВАРИАНТА')
                continue

    def show_balance(self, login):
        id_user = cur.execute('SELECT id FROM users WHERE username=?', (login, )).fetchone()[0]
        balance_user = cur.execute('SELECT amount FROM balance WHERE user_id=?', (id_user,)).fetchone()[0]
        print('*' * 30)
        print(f'На вашем счету {balance_user} грн.')
        print('*' * 30)

    def add_balance(self, login):
        id_user = cur.execute('SELECT id FROM users WHERE username=?', (login,)).fetchone()[0]
        balance_user = cur.execute('SELECT amount FROM balance WHERE user_id=?', (id_user,)).fetchone()[0]
        how = int(input('На сколько желаете пополнить?: '))
        result = balance_user + abs(how)
        cur.execute('UPDATE balance SET amount=? WHERE user_id=?', (result, id_user))
        con.commit()
        text = f'На Ваш баланс внесено {how} ГРН.'
        self.transaction(login, text)

    def withdraw_balance(self, login):
        id_user = cur.execute('SELECT id FROM users WHERE username=?', (login,)).fetchone()[0]
        balance_user = cur.execute('SELECT amount FROM balance WHERE user_id=?', (id_user,)).fetchone()[0]
        atm_nominal = cur.execute('SELECT * FROM balance_atm').fetchall()
        what_is_nominal = {}    # словарь со всем номиналом в банкомате, даже если купюр 0
        for i in atm_nominal:
            what_is_nominal[i[0]] = i[1]
        what_is_nominal_out = [int(i) for i in what_is_nominal.keys() if what_is_nominal[i] != 0] # весь доступный номинал (>0)
        print('Доступен номинал:')
        for i in what_is_nominal_out:
            print(f'{i}', end=', ')

        how = abs(int(input('\nСколько желаете снять?: ')))

        balance_atm = sum([int(i[0]) * i[1] for i in atm_nominal])
        if how > balance_user:
            text = 'Не достаточно денег на Вашем балансе!'
            print('НЕ ДОСТАТОЧНО ДЕНЕГ НА БАЛАНСЕ!')
            self.transaction(login, text)
        elif how > balance_atm:
            text = 'Банкомат не может выдать такую сумму!'
            print('НЕ ДОАСТАТОЧНО ДЕНЕГ В БАНКОМАТЕ!')
            self.transaction(login, text)
        else:
            out = {'1000': 0, '500': 0, '200': 0, '100': 0, '50': 0, '20': 0, '10': 0}
            inquiry = how

            flag = True
            while flag:
                flag = False
                if inquiry // 1000 > 0 and what_is_nominal['1000'] != 0 and \
                        ((inquiry - 1000) == 0 or [i for i in what_is_nominal_out if ((inquiry - 1000) // i) > 0]):
                    what_is_nominal['1000'] -= 1
                    out['1000'] += 1
                    inquiry -= 1000
                    if inquiry == 0:
                        break
                    else:
                        flag = True
                elif inquiry // 500 > 0 and what_is_nominal['500'] != 0 and \
                        ((inquiry - 500) == 0 or [i for i in what_is_nominal_out if ((inquiry - 500) // i) > 0]):
                    what_is_nominal['500'] -= 1
                    out['500'] += 1
                    inquiry -= 500
                    if inquiry == 0:
                        break
                    else:
                        flag = True
                elif inquiry // 200 > 0 and what_is_nominal['200'] != 0 and \
                        ((inquiry - 200) == 0 or [i for i in what_is_nominal_out if ((inquiry - 200) // i) > 0]):
                    what_is_nominal['200'] -= 1
                    out['200'] += 1
                    inquiry -= 200
                    if inquiry == 0:
                        break
                    else:
                        flag = True
                elif inquiry // 100 > 0 and what_is_nominal['100'] != 0 and \
                        ((inquiry - 100) == 0 or [i for i in what_is_nominal_out if ((inquiry - 100) // i) > 0]):
                    what_is_nominal['100'] -= 1
                    out['100'] += 1
                    inquiry -= 100
                    if inquiry == 0:
                        break
                    else:
                        flag = True
                elif inquiry // 50 > 0 and what_is_nominal['50'] != 0 and \
                        ((inquiry - 50) == 0 or [i for i in what_is_nominal_out if ((inquiry - 50) // i) > 0]):
                    what_is_nominal['50'] -= 1
                    out['50'] += 1
                    inquiry -= 50
                    if inquiry == 0:
                        break
                    else:
                        flag = True
                elif inquiry // 20 > 0 and what_is_nominal['20'] != 0 and \
                        ((inquiry - 20) == 0 or [i for i in what_is_nominal_out if ((inquiry - 20) // i) > 0]):
                    what_is_nominal['20'] -= 1
                    out['20'] += 1
                    inquiry -= 20
                    if inquiry == 0:
                        break
                    else:
                        flag = True
                elif inquiry // 10 > 0 and what_is_nominal['10'] != 0 and \
                        ((inquiry - 10) == 0 or [i for i in what_is_nominal_out if ((inquiry - 10) // i) > 0]):
                    what_is_nominal['10'] -= 1
                    out['10'] += 1
                    inquiry -= 10
                    if inquiry == 0:
                        break
                    else:
                        flag = True

            result = [int(k) * v for k, v in out.items()]
            if sum(result) == how:
                res = {}
                for k, v in out.items():
                    if v == 0:
                        continue
                    res[k] = v
                print(f'Вам выдано {sum(result)}')
                print('Номиналами:')
                for k, v in res.items():
                    print(f'{k}x{v}', end=' ')
                print('\n')

                what_is_nominal_list = []
                for k, v in what_is_nominal.items():
                    what_is_nominal_list.append((v, k))
                for nom in what_is_nominal_list:
                    cur.execute('UPDATE balance_atm SET number=? WHERE nominal=?', nom)
                    con.commit()

                result_after = balance_user - sum(result)
                cur.execute('UPDATE balance SET amount=? WHERE user_id=?', (result_after, id_user))
                con.commit()
                text = f'{how} грн снято с Вашего баланса.'
                self.transaction(login, text)
            else:
                text = 'There are no matching bills at the ATM!!!'
                self.transaction(login, text)
                print('БАНКОМАТ НЕ МОЖЕТ ВЫДАТЬ ДАННУЮ СУММУ!!!')

    # Общие блоки кода
    def transaction(self, login, text):
        text = text
        time = str(dt.datetime.now())
        cur.execute('INSERT INTO transactions (user, date, massage) VALUES (?, ?, ?)', (login, time, text))
        con.commit()

    def show_currency(self):
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
        response = requests.get(url)

        currency = json.loads(response.text)

        print('-' * 30)
        for curr in currency:
            info = f'{curr["ccy"]} -> {curr["base_ccy"]}: buy {curr["buy"]}, sale {curr["sale"]}'
            print(info)
        print('-' * 30)





if __name__ == '__main__':
    atm = ATM()
    atm.menu_start()
    con.close()