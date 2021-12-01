'''На основі попередньої функції створити наступний кусок кода:
а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по правилам своєї функції) -
як валідні, так і ні;
б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором, перевірить ці дані
і надрукує для кожної пари значень відповідне повідомлення, наприклад:
    Name: vasya
    Password: wasd
    Status: password must have at least one digit
    -----
    Name: vasya
    Password: vasyapupkin2000
    Status: OK
P.S. Не забудьте використати блок try/except ;)'''

class BadLogin(Exception):
    def __init__(self, msg):
        self.msg_login = msg

class BadPass(Exception):
    def __init__(self, msg):
        self.msg_pass = msg


def validation(username, password):
    if len(username) < 3 or len(username) > 50:
        raise BadLogin('Login must be in the range from 3 to 50')
    elif len(str(password)) < 8:
        raise BadPass('Pass is short')
    elif bool([pas_wd for pas_wd in str(password) if pas_wd.isdigit()]) == False:
        raise BadPass('Password must have at least one digit')
    elif bool([pas_wd for pas_wd in str(password) if pas_wd.isupper()]) == False:
        raise BadPass('Еhe password must have at least one capital letter')
    else:
        return 'Registration successful'

logins = [('Vitalii', 12345), ('Valera', 'paSs123word'), ('te', 'test'), ('admin', 'admindjfhklla'), ('root', 99384775456)]

for login in logins:
    try:
        validation(login[0], login[1])
        print(f'Name: {login[0]}')
        print(f'Password: {login[1]}')
        print('Status: OK')
        print('-' * 10)
    except BadLogin as msg:
        print(f'Name: {login[0]}')
        print(f'Password: {login[1]}')
        print('Status: ' + msg.msg_login)
        print('-' * 10)
    except BadPass as msg:
        print(f'Name: {login[0]}')
        print(f'Password: {login[1]}')
        print('Status: ' + msg.msg_pass)
        print('-' * 10)

