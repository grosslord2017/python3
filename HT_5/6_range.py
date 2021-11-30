'''Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
P.S. Повинен вертатись генератор.
P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній:
https://docs.python.org/3/library/stdtypes.html#range'''

def my_range(*args):
    if len(args) == 3:
        start = args[0]
        finish = args[1]
        step = args[2]
    elif len(args) == 2:
        start = args[0]
        finish = args[1]
        step = 1
    elif len(args) == 1:
        start = 0
        finish = args[0]
        step = 1
    else:
        raise TypeError
    result = []
    count = start
    while count < finish:
        result.append(count)
        count += step
    return result

print(my_range(10))
print(my_range(3, 10))
print(my_range(2, 10, 3))