'''Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну цифру;
   - щось своє :)
   Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.'''

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

#validation('Vitalii', 12345)
validation('Valera', 'pAss123word')
#validation('te', 'test')
#validation('admin', 'admindjfhklla')
#validation('root', 99384775456)