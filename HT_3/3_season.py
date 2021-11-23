'''Написати функцiю season, яка приймає один аргумент — номер мiсяця (вiд 1 до 12),
яка буде повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь)'''

def season(number):
    if number in [12, 1, 2]:
        print('winter')
    elif number in [3, 4, 5]:
        print('spring')
    elif number in [6, 7, 8]:
        print('summer')
    elif number in [9, 10, 11]:
        print('autumn')

number = int(input('Enter number of month: '))

season(number)