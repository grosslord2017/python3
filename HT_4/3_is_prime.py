'''Написати функцию < is_prime >, яка прийматиме 1 аргумент - число
від 0 до 1000, и яка вертатиме True, якщо це число просте, и False - якщо ні.'''

def is_prime(number):
    exam = 2
    while number % exam != 0:
        exam += 1
    return exam == number

print(is_prime(12))
print(is_prime(997))
