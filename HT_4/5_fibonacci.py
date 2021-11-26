'''Написати функцію < fibonacci >, яка приймає один аргумент і виводить
всі числа Фібоначчі, що не перевищують його.'''


def fibonacci(number):
    fibonacci_list = [0, 1]
    while True:
        sum_elems = fibonacci_list[-1] + fibonacci_list[-2]
        if sum_elems < number:
            fibonacci_list.append(sum_elems)
        else:
            break
    return fibonacci_list

print(fibonacci(48))
