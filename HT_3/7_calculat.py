'''Калькулятор :) повинна бути 1 ф-цiя яка б приймала 3 аргументи - один з яких операцiя,
яку зробити!'''

def calc(number_1, symbol, number_2):
    if symbol == '+':
        print(int(number_1) + int(number_2))
    elif symbol == '-':
        print(int(number_1) - int(number_2))
    elif symbol == '*':
        print(int(number_1) * int(number_2))
    elif symbol == '/':
        print(int(number_1) / int(number_2))

expression = input('Enter your expression (in format a + b for example): \n').split()
number_1, symbol, number_2 = expression

calc(number_1, symbol, number_2)