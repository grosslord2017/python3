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

# Сlass creates a database with standard tables and users
class StartDbAtm(object):
    '''Сlass creates a database with standard tables and users'''
    def __init__(self):
        self.con = sqlite3.connect('ATM.db')
        self.cur = self.con

    def default_users(self):
        users = [
            ('user1', 'user1', False),
            ('user2', 'user2', False),
            ('admin', 'admin', True),
        ]
        for user in users:
            exists = self.cur.execute('''SELECT id FROM users WHERE username=?''', (user[0],)).fetchone()
            if not exists:
                self.cur.execute('INSERT INTO users (username, password, is_incasator) VALUES (?, ?, ?);', user)
                self.con.commit()
                user_id = self.cur.execute('''SELECT id FROM users WHERE username=?''', (user[0],)).fetchone()[0]
                self.cur.execute('INSERT INTO balance (user_id, amount) VALUES (?, ?);', (user_id, 0))
                self.con.commit()
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
            exists = self.cur.execute('''SELECT nominal FROM balance_atm WHERE nominal=?''', (nominal[0],)).fetchone()
            if not exists:
                self.cur.execute('INSERT INTO balance_atm (nominal, number) VALUES (?, ?)', nominal)
                self.con.commit()

    def create_table(self):
        # users
        self.cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id integer NOT NULL PRIMARY KEY,
        username text NOT NULL,
        password text NOT NULL,
        is_incasator bit DEFAULT false
    );
    ''')
        # balance
        self.cur.execute('''
    CREATE TABLE IF NOT EXISTS balance (
        user_id integer NOT NULL,
        amount float NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    ''')
        # balance_atm
        self.cur.execute('''
    CREATE TABLE IF NOT EXISTS balance_atm (
        nominal text NOT NULL,
        number integer NOT NULL DEFAULT 10
    );
    ''')
        # transactions
        self.cur.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        user text NOT NULL,
        date text NOT NULL,
        massage text NOT NULL,
        FOREIGN KEY (user) REFERENCES users (username)
    );
    ''')

class Authorization(object):

    def __init__(self, cur):
        self.cur = cur

    def autorization(self):
        count = 3
        for i in range(3):
            login = input('Enter your login: ')
            password = input('Enter your password: ')
            user = (login, password)
            user_in_db = self.cur.execute(
                '''SELECT username, password, is_incasator FROM users WHERE username=? AND password=?''',
                user).fetchone()
            if user_in_db:
                if user_in_db[2] == 1:
                    print('STATUS INCASATOR')
                else:
                    print('STATUS OK')
                return user_in_db[0], user_in_db[2]
            else:
                count -= 1
                print(f'--- Your Login or Password is wrong {count} ---')
                continue
        raise BadOuth('Wrong login or password!!!')

    def registration(self):
        login = input('Create login: ')
        password = input('Create password: ')
        user = (str(login), str(password))
        user_in_db = self.cur.execute('''SELECT username FROM users WHERE username=? AND password=?''', user).fetchall()
        if not user_in_db:
            self.cur.execute('INSERT INTO users (username, password) VALUES (?, ?);', user)
            StartDbAtm().con.commit()
            user_id = self.cur.execute('''SELECT id FROM users WHERE username=?''', (user[0],)).fetchone()[0]
            self.cur.execute('INSERT INTO balance (user_id, amount) VALUES (?, ?);', (user_id, 0))
            db.con.commit()
            print('--- User Created saccess. ---')
        else:
            print('--- Login in busy, please try again. ---')

class User(object):
    def __init__(self, cur, login):
        self.login = login
        self.cur = cur

    def menue_user(self):
        while True:
            print('1 - view the balance.')
            print('2 - add in to your balance.')
            print('3 - withdrawing from the balance.')
            print('4 - return to the previous menu.')
            print('5 - exit program.')
            choice = input('Your choice: ')
            if choice == '1':
                self.show_balance()
            elif choice == '2':
                self.add_balance()
            elif choice == '3':
                self.withdraw_balance()
            elif choice == '4':
                break
            elif choice == '5':
                print('Thank you for using our ATM!')
                exit()
            else:
                print('THERE IS NO SUCH OPTION')
                continue

    def show_balance(self):
        id_user = self.cur.execute('SELECT id FROM users WHERE username=?', (self.login,)).fetchone()[0]
        balance_user = self.cur.execute('SELECT amount FROM balance WHERE user_id=?', (id_user,)).fetchone()[0]
        print('*' * 30)
        print(f'On your account {balance_user} uah.')
        print('*' * 30)

    def add_balance(self):
        id_user = self.cur.execute('SELECT id FROM users WHERE username=?', (self.login,)).fetchone()[0]
        balance_user = self.cur.execute('SELECT amount FROM balance WHERE user_id=?', (id_user,)).fetchone()[0]
        how = int(input('How much do you want to top up your account?: '))
        result = balance_user + abs(how)
        self.cur.execute('UPDATE balance SET amount=? WHERE user_id=?', (result, id_user))
        db.con.commit()
        text = f'На Ваш баланс внесено {how} ГРН.'
        atm.transaction(self.login, text)

    def withdraw_balance(self):
        id_user = self.cur.execute('SELECT id FROM users WHERE username=?', (self.login,)).fetchone()[0]
        balance_user = self.cur.execute('SELECT amount FROM balance WHERE user_id=?', (id_user,)).fetchone()[0]
        atm_nominal = self.cur.execute('SELECT * FROM balance_atm').fetchall()
        what_is_nominal = {}    # словарь со всем номиналом в банкомате, даже если купюр 0
        for i in atm_nominal:
            what_is_nominal[i[0]] = i[1]
        what_is_nominal_out = [int(i) for i in what_is_nominal.keys() if what_is_nominal[i] != 0] # весь доступный номинал (>0)
        print('available denomination:')
        for i in what_is_nominal_out:
            print(f'{i}', end=', ')

        how = abs(int(input('\nhow much would you like to rent?: ')))

        balance_atm = sum([int(i[0]) * i[1] for i in atm_nominal])
        if how > balance_user:
            text = 'Не достаточно денег на Вашем балансе!'
            print('NOT ENOUGH MONEY INTO YOUR BALANCE!')
            atm.transaction(self.login, text)
        elif how > balance_atm:
            text = 'Банкомат не может выдать такую сумму!'
            print('NOT ENOUGH MONEY IN ATM!')
            atm.transaction(self.login, text)
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
                print(f'you have been given cash {sum(result)}')
                print('denominations:')
                for k, v in res.items():
                    print(f'{k}x{v}', end=' ')
                print('\n')

                what_is_nominal_list = []
                for k, v in what_is_nominal.items():
                    what_is_nominal_list.append((v, k))
                for nom in what_is_nominal_list:
                    self.cur.execute('UPDATE balance_atm SET number=? WHERE nominal=?', nom)
                    db.con.commit()

                result_after = balance_user - sum(result)
                self.cur.execute('UPDATE balance SET amount=? WHERE user_id=?', (result_after, id_user))
                db.con.commit()
                text = f'{how} грн снято с Вашего баланса.'
                atm.transaction(self.login, text)
            else:
                text = 'There are no matching bills at the ATM!!!'
                atm.transaction(self.login, text)
                print('ATM CANNOT DISPOSE THIS AMOUNT !!!')

class Incasation(object):
    def __init__(self, cur):
        self.cur = cur

    def menu_incasation(self):
        while True:
            print('1 - view the ATM balance')
            print('2 - add in to ATM')
            print('3 - exit')
            choice_inc = input('Your choice: ')
            if choice_inc == '1':
                self.show_balance()
            elif choice_inc == '2':
                self.add_balance()
            elif choice_inc == '3':
                exit()
            else:
                print('There are no such options!')
                continue

    def add_balance(self):
        nominals = self.cur.execute('SELECT * FROM balance_atm').fetchall()
        nominal = {}
        for i in nominals:
            nominal[i[0]] = i[1]
        while True:
            addition = input('Enter the denomination and quantity (example: 1000, 10) or enter exit: ')
            if addition == 'exit':
                 break
            addition = addition.split(', ') #['1000', '10']
            if addition[0] not in ['1000', '500', '200', '100', '50', '20', '10']:
                print('THERE IS NO SUCH DENOMINATION.')
                continue
            nominal[addition[0]] += abs(int(addition[1]))
            self.cur.execute('UPDATE balance_atm SET number=? WHERE nominal=?', (nominal[addition[0]], addition[0]))
            db.con.commit()

    def show_balance(self):
        nominals = self.cur.execute('SELECT * FROM balance_atm').fetchall()
        nominal = {}
        for i in nominals:
            nominal[i[0]] = i[1]

        print('Denomination:')
        for k, v in nominal.items():
            print(f'{k.ljust(6)}{str(v).rjust(5)}')
        print('*' * 50)

class Atm(object):
    def __init__(self, cur):
        self.cur = cur

    def menue_start(self):
        while True:
            print('1 - registration')
            print('2 - authorization')
            print('3 - current exchange rate')
            print('4 - exit')
            choice = input('Your choice: ')
            if choice == '1':
                person = Authorization(self.cur)
                person.registration()
            elif choice == '2':
                person = Authorization(self.cur)
                login, incasation = person.autorization()
                if incasation:
                    incasation = Incasation(db.cur)
                    incasation.menu_incasation()
                else:
                    user = User(self.cur, login)
                    user.menue_user()
            elif choice == '3':
                self.show_currency()
            elif choice == '4':
                exit()
            else:
                print('there is no such option!')

    def show_currency(self):
        url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
        response = requests.get(url)

        currency = json.loads(response.text)

        print('-' * 30)
        for curr in currency:
            info = f'{curr["ccy"]} -> {curr["base_ccy"]}: buy {curr["buy"]}, sale {curr["sale"]}'
            print(info)
        print('-' * 30)

    def transaction(self, login, text):
        text = text
        time = str(dt.datetime.now())
        self.cur.execute('INSERT INTO transactions (user, date, massage) VALUES (?, ?, ?)', (login, time, text))
        db.con.commit()




if __name__ == '__main__':
    db = StartDbAtm()
    db.create_table()
    db.default_users()
    atm = Atm(db.cur)
    atm.menue_start()
