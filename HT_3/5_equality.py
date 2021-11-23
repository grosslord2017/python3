'''Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями;
-  Створiть просту умовну конструкцiю(звiсно вона повинна бути в тiлi ф-цiї),
пiд час виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y" і при нерiвностi змiнних
"х" та "у" вiдповiдь повертали рiзницю чисел.
-  Повиннi опрацювати такi умови:
-  x > y; вiдповiдь - х бiльше нiж у на z
-  x < y; вiдповiдь - у бiльше нiж х на z
-  x == y. вiдповiдь - х дорiвнює z'''

def equality(x, y):
    if x > y:
        return f'{x} больше чем {y} на {x - y}'
    elif x < y:
        return f'{y} больше чем {x} на {y - z}'
    elif x == y:
        return f'{x} равно {y}'

numb_x = int(input('Enter x: '))
numb_y = int(input('Enter y: '))

result = equality(numb_x, numb_y)
print(result)