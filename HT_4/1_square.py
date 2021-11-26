'''Написати функцію < square > , яка прийматиме один аргумент - сторону
квадрата, і вертатиме 3 значення (кортеж):
периметр квадрата, площа квадрата та його діагональ.'''

from math import sqrt

def square(side):
    result = []
    result.append(side * 4) # perimeter
    result.append(side ** 2) # square
    result.append(sqrt(2 * side ** 2)) # diagonal
    return tuple(result)


print(square(5))
