'''Написати скрипт, який буде приймати від користувача назву валюти і початкову дату.
   - Перелік валют краще принтануть.
   - Також не забудьте указати, в якому форматі коритувач повинен ввести дату.
   - Додайте перевірку, чи введена дата не знаходиться у майбутньому ;)
   - Також перевірте, чи введена правильна валюта.
   Виконуючи запроси до API архіву курсу валют Приватбанку, вивести інформацію про зміну
   курсу обраної валюти (Нацбанк) від введеної дати до поточної.'''

'''Данный скрипт работает с валютой USD, EUR, RUB
Не стал нагромождать его остальными видами валюты.'''

import requests
import datetime as dt
from time import sleep
import json


def rate_archive():
    # блок ввода от пользователя и проверка актуальности даты.
    print('Available currency: USD, EUR, RUB')
    currency = input('Select the currency you want to track: ')

    if currency not in ['USD', 'usd', 'Usd', 'EUR', 'eur', 'Eur', 'RUB', 'rub', 'Rub']:
        print("I CAN'T SHOW OTHER CURRRENCY!!!")
        return

    moment = input('Enter date in format dd.mm.yyyy: ')
    date_now = dt.datetime.now()
    try:
        moment_format = dt.datetime.strptime(moment, "%d.%m.%Y")
    except ValueError:
        print('INVALID FORMAT')
        return

    delta = dt.timedelta(days=1)

    if moment_format > date_now:
        print("I CAN'T TAKE Exchange Rates IN FUTURE!!!")
        return

    new_moment = moment
    new_moment_format = moment_format
    nbu = 0

    print(f'Currency: {currency}')
    while new_moment_format < date_now:
        url = 'https://api.privatbank.ua/p24api/exchange_rates?json&date=' + f'{new_moment}'
        response = requests.get(url)
        rate = json.loads(response.text)['exchangeRate']

        for r in rate:
            if 'currency' not in [i for i in r.keys()]:
                continue
            elif r['currency'] == currency:
                print(f'Date: {new_moment}')
                if nbu == 0:
                    print(f'NBU: {r["saleRateNB"]}     ------')
                else:
                    print(f'NBU: {r["saleRateNB"]}     {float(r["saleRateNB"]) - nbu}')
                print('-' * 30)
                nbu = float(r["saleRateNB"])
                sleep(1)

        a = new_moment_format + delta
        new_moment_format = a
        temp = str(dt.datetime.date(new_moment_format)).split('-')
        new_moment = f'{temp[2]}.{temp[1]}.{temp[0]}'
    exit()


while True:
    rate_archive()
