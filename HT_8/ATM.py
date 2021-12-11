'''Банкомат с интуитивно понятным интерфейсом
для входа в систему инкасатора поспользуйтесь логином и паролем приведеным ниже.
логин: ADMIN
пароль: ADMIN'''

import csv
import json
import datetime as dt
import os

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

def registration():
    login = input('Придумайте и введите логин: ')
    password = input('Придумайте и введите пароль: ')
    user = [str(login), str(password)]
    registration_user = []
    with open(path + 'user.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i in reader:
            registration_user.append(i)
    for reg_user in registration_user:
        if login == reg_user[0]:
            # raise LoginIsBusy('Логин уже занят')
            print('--- Логин уже занят ---')
            break
    with open(path + 'user.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(user)
    with open(path + login + '.txt', 'w') as file:
        file.write('0')

def autorization():
    count = 3
    for i in range(3):
        login = input('Введите ваш логин: ')
        password = input('Введите ваш пароль: ')
        user = [login, password]
        registration_user = []
        with open(path + 'user.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i in reader:
                registration_user.append(i)
        if user == ['ADMIN', 'ADMIN']:
            print('STATUS INCASATION')
            return login, password, True
        elif user in registration_user:
            print('STATUS OK')
            return login, password, False
        else:
            count -= 1
            print(f'--- Логин или пароль не верный, попыток осталось {count} ---')
            continue

    raise BadOuth('Не верный логин или пароль!!!')

# Ниже код для работы инкасатора.
def menu_start():
    while True:
        print('1 - для регистрации')
        print('2 - для авторизации')
        print('3 - для выхода из программы')
        choice = input('Ваш выбор: ')
        if choice == '1':
            registration()
        elif choice == '2':
            login, password, incasation = autorization()
            if incasation:
                menu_incasation()
            else:
                menu_user(login)
        elif choice == '3':
            exit()
        else:
            print('НЕТ ТАКОГО ВАРИАНТА.')

def menu_incasation():
    while True:
        print('1 - для вывода остатка средств в банкомате')
        print('2 - для добавления денег в банкомат')
        print('3 - для выхода')
        choice_inc = input('Ваш выбор: ')
        if choice_inc == '1':
            show_balance_atm()
        elif choice_inc == '2':
            add_balance_atm()
        elif choice_inc == '3':
            exit()
        else:
            print('Таких вариантов нет!')
            continue

def show_balance_atm():
    with open(path + 'nominal.json', 'r') as file:
        reader = json.load(file)
        print('Номинал:')
        for k, v in reader.items():
            print(f'{k.ljust(6)}{str(v).rjust(5)}')
    print('*' * 50)

def add_balance_atm():
    with open(path + 'nominal.json', 'r') as file:
        writer = json.load(file)
    while True:
        addition = input('Введите номинал и количество (пример: 1000, 10) или введите exit: ')  # ['1000', '10']
        if addition == 'exit':
            break
        addition = addition.split(', ')
        if addition[0] not in ['1000', '500', '200', '100', '50', '20', '10']:
            print('НЕТ ТАКОГО НОМИНАЛА.')
            continue
        writer[addition[0]] += abs(int(addition[1]))
        with open(path + 'nominal.json', 'w') as file:
            file.write(json.dumps(writer))


# Ниже код для работы с пользователем.
def menu_user(login):
    while True:
        print('1 - для просмотра баланса.')
        print('2 - для пополнения баланса.')
        print('3 - для снятия средств с баланса.')
        print('4 - для возвращения в предыдущее меню.')
        print('5 - для выхода из программы.')
        choice = input('Ваш выбор: ')
        if choice == '1':
            show_balance(login)
        elif choice == '2':
            add_balance(login)
        elif choice == '3':
            withdraw_balance(login)
        elif choice == '4':
            break
        elif choice == '5':
            print('Спасибо что воспользовались нашим банкоматом!')
            exit()
        else:
            print('НЕТ ТАКОГО ВАРИАНТА')
            continue

def show_balance(login):
    with open(path + login + '.txt', 'r') as file:
        reader = file.read()
        print('*' * 30)
        print(f'На вашем счету {reader} грн.')
        print('*' * 30)

def add_balance(login):
    with open(path + login + '.txt', 'r') as file:
        balance = int(file.read())
        how = int(input('На сколько желаете пополнить?: '))
    with open(path + login + '.txt', 'w') as file:
        file.write(str(balance + abs(how)))
        text = f'Your personal account has been credited to {how} UAH.'
        transaction(login, text)

def withdraw_balance(login):
    with open(path + login + '.txt', 'r') as file:
        balance = int(file.read())
    with open(path + 'nominal.json', 'r') as file:
        reader = json.load(file)

    what_is_nominal = [int(i) for i in reader.keys()]
    print('Доступен номинал:')
    for i in what_is_nominal:
        print(f'{i}', end=', ')
    how = abs(int(input('\nСколько желаете снять?: ')))

    sum_in_atm = sum([int(k) * v for k, v in reader.items()])
    nom = [int(i) for i in reader.keys() if reader[i] != 0]
    if how > balance:
        text = 'Not enough money on the balance sheet!!!'
        transaction(login, text)
        print('НЕ ДОСТАТОЧНО ДЕНЕГ НА БАЛАНСЕ!')
    elif how > sum_in_atm:
        text = 'The ATM cannot dispense this amount of money!!!'
        transaction(login, text)
        print('НЕ ДОАСТАТОЧНО ДЕНЕГ В БАНКОМАТЕ!')
    else:
        out = {'1000': 0, '500': 0, '200': 0, '100': 0, '50': 0, '20': 0, '10': 0}
        inquiry = how

        flag = True
        while flag:
            flag = False
            if inquiry // 1000 > 0 and reader['1000'] != 0 and \
                    ((inquiry - 1000) == 0 or [i for i in nom if ((inquiry - 1000) // i) > 0]):
                reader['1000'] -= 1
                out['1000'] += 1
                inquiry -= 1000
                if inquiry == 0:
                    break
                else:
                    flag = True
            elif inquiry // 500 > 0 and reader['500'] != 0 and \
                    ((inquiry - 500) == 0 or [i for i in nom if ((inquiry - 500) // i) > 0]):
                reader['500'] -= 1
                out['500'] += 1
                inquiry -= 500
                if inquiry == 0:
                    break
                else:
                    flag = True
            elif inquiry // 200 > 0 and reader['200'] != 0 and \
                    ((inquiry - 200) == 0 or [i for i in nom if ((inquiry - 200) // i) > 0]):
                reader['200'] -= 1
                out['200'] += 1
                inquiry -= 200
                if inquiry == 0:
                    break
                else:
                    flag = True
            elif inquiry // 100 > 0 and reader['100'] != 0 and \
                    ((inquiry - 100) == 0 or [i for i in nom if ((inquiry - 100) // i) > 0]):
                reader['100'] -= 1
                out['100'] += 1
                inquiry -= 100
                if inquiry == 0:
                    break
                else:
                    flag = True
            elif inquiry // 50 > 0 and reader['50'] != 0 and \
                    ((inquiry - 50) == 0 or [i for i in nom if ((inquiry - 50) // i) > 0]):
                reader['50'] -= 1
                out['50'] += 1
                inquiry -= 50
                if inquiry == 0:
                    break
                else:
                    flag = True
            elif inquiry // 20 > 0 and reader['20'] != 0 and \
                    ((inquiry - 20) == 0 or [i for i in nom if ((inquiry - 20) // i) > 0]):
                reader['20'] -= 1
                out['20'] += 1
                inquiry -= 20
                if inquiry == 0:
                    break
                else:
                    flag = True
            elif inquiry // 10 > 0 and reader['10'] != 0 and \
                    ((inquiry - 10) == 0 or [i for i in nom if ((inquiry - 10) // i) > 0]):
                reader['10'] -= 1
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
            with open(path + 'nominal.json', 'w') as file:
                file.write(json.dumps(reader))
            with open(path + login + '.txt', 'w') as file:
                file.write(str(balance - how))
            text = f'{how} UAH was debited from your account'
            transaction(login, text)
        else:
            text = 'There are no matching bills at the ATM!!!'
            transaction(login, text)
            print('БАНКОМАТ НЕ МОЖЕТ ВЫДАТЬ ДАННУЮ СУММУ!!!')

# Общие блоки кода
def transaction(login, text):
    with open(path + login + '_transaction.jsonlines', 'a', encoding='utf-8') as file:
        massage = {str(dt.datetime.now()): text}
        json.dump(massage, file)
        file.write('\n')



menu_start()