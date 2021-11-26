'''Вводиться число. Якщо це число додатне, знайти його квадрат, якщо від'ємне,
збільшити його на 100, якщо дорівнює 0, не змінювати.'''

def action(number):
    if number > 0:
        return number ** 2
    elif number < 0:
        return number + 100
    elif number == 0:
        return number

number = int(input('Enter your number: '))
print(action(number))
