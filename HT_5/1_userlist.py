'''Створіть функцію, всередині якої будуть записано список із п'яти користувачів (ім'я та пароль).
Функція повинна приймати три аргументи: два - обов'язкових (<username> та <password>) і третій -
необов'язковий параметр <silent> (значення за замовчуванням - <False>).
Логіка наступна:
якщо введено коректну пару ім'я/пароль - вертається <True>;
якщо введено неправильну пару ім'я/пароль і <silent> == <True> - функція вертає <False>,
інакше (<silent> == <False>) - породжується виключення LoginException'''

class LoginExeption(Exception):
    pass

def user_outh(username, password, silent=False):
    users = [('Vitalii', 12345), ('Valera', 998833), ('test', 'test'), ('admin', 'admin'), ('root', 99384775)]

    if (username, password) in users:
        return True
    elif (username, password) not in users and silent == True:
        return False
    else:
        raise LoginExeption('нет такого юзера')

print(user_outh('Valeraа', 998833, True))
