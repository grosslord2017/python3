'''Програма-банкомат.
   Створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.data>);
      - кожен з користувачів має свій поточний баланс (файл <{username}_balance.data>) та історію транзакцій
      (файл <{username}_transactions.data>);
      - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних (введено число;
      знімається не більше, ніж є на рахунку).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
      - файл з користувачами: тільки читається. Якщо захочете реалізувати функціонал додавання нового користувача -
      не стримуйте себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь workflow банкомата:
      - спочатку - логін користувача - програма запитує ім'я/пароль. Якщо вони неправильні - вивести повідомлення про
      це і закінчити роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :) )
      - потім - елементарне меню типа:
        Введіть дію:
           1. Продивитись баланс
           2. Поповнити баланс
           3. Вихід
      - далі - фантазія і креатив :)'''

import csv
import datetime

class BadOuth(Exception):
    def __init__(self, msg):
        self.msg = msg

class LoginIsBusy(Exception):
    def __init__(self, msg):
        self.msg = msg

def start():
    print('Пожалуйста авторизируйтесь!')
    login = input('Введите ваш логин: ')
    password = input('Введите ваш пароль: ')
    autorization(login, password)
    print('Введите 1 для просмотра баланса.')
    print('Введите 2 для пополнения баланса.')
    print('Введите 3 для снятия средств с баланса.')
    print('Введите 4 для выхода')
    choice = input('Ваш выбор: ')
    if choice == '1':
        show_balance(login)
    elif choice == '2':
        number = int(input('Введите число, на которое хотите пополнить баланс: '))
        add_balance(login, number)
    elif choice == '3':
        number = int(input('Введите суму, которую хотите снять: '))
        withdraw_balance(login, number)
    elif choice == '4':
        print('Спасибо что воспользовались нашим банкоматом!')
        exit()

def registration():
    login = input('Придумайте и введите логин: ')
    password = input('Придумайте и введите пароль: ')
    user = [str(login), str(password)]
    registration_user = []
    with open('user.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i in reader:
            registration_user.append(i)
    for reg_user in registration_user:
        if login == reg_user[0]:
            raise LoginIsBusy('Логин уже занят')
    with open('user.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(user)
    with open(login + '.txt', 'w') as file:
        file.write('0')

def autorization(login, password):
    user = [str(login), str(password)]
    registration_user = []
    with open('user.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for i in reader:
            registration_user.append(i)
    if user in registration_user:
        print('STATUS OK')
    else:
        raise BadOuth('Не верный логин или пароль!!!')

def show_balance(login):
    with open(login + '.txt', 'r') as file:
        balance = file.read()
        print(f'На вашем счету {balance} грн.')
    cont_inue()

def add_balance(login, number):
    with open(login + '.txt', 'r') as file:
        money = int(file.read())
    with open(login + '.txt', 'w') as file:
        file.write(str(money + number))
    text = 'Ваш счет пополнен на'
    transactions(login, number, text)
    cont_inue()

def withdraw_balance(login, number):
    with open(login + '.txt', 'r') as file:
        money = int(file.read())
    with open(login + '.txt', 'w') as file:
        if money < number:
            print('Не достаточно денег на счету.')
            file.write(str(money))
            text = 'Неудачная попытка списать '
            transactions(login, number, text)
        else:
            file.write(str(money - number))
            text = 'С Вашего счета списано'
            transactions(login, number, text)
    cont_inue()

def cont_inue():
    print('Желаете продолжить?')
    print('Для продолжения введите Y, для выхода введите N')
    yes_no = input('Ваш выбор: ')
    if yes_no in ['N', 'n', 'no', 'NO', 'No']:
        exit()

def transactions(login, number, text):
    with open(login + '_transaction.txt', 'a') as file:
        writer = file.write(f'{datetime.datetime.now()}: {text} {number} грн.\n')

print('Привеитствую')
print('Если вы желаете авторизироватся - введите 1')
print('Если вы желаете зарегистрироватся - введите 2')
print('Для выхода - введите 3')

reg = input('Ваш выбор: ')
if reg == '1':
    while True:
        start()
elif reg == '2':
    registration()
else:
    exit()

# while True:
#     start()