'''Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
   - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
   - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну цифру;
   - щось своє :)
   Якщо якийсь із параментів не відповідає вимогам - породити виключення із відповідним текстом.'''

class BadLogin(Exception):
    msg_login = 'Login must be in the range from 3 to 50'

class BadPassShort(Exception):
    msg_short = 'Pass is short'

class BadPassDigit(Exception):
    msg_digit = 'Password must have at least one digit'


def validation(username, password):
    if len(username) < 3 or len(username) > 50:
        raise BadLogin('Login must be in the range from 3 to 50')
    elif len(str(password)) < 8:
        raise BadPassShort('Pass is short')
    elif bool([pas_wd for pas_wd in str(password) if pas_wd.isdigit()]) == False:
        raise BadPassDigit('Password must have at least one digit')
    else:
        return 'Registration successful'

#validation('Vitalii', 12345)
#validation('Valera', 'pass123word')
#validation('te', 'test')
#validation('admin', 'admindjfhklla')
validation('root', 99384775456)