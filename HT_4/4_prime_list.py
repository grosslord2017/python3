'''Написати функцію < prime_list >, яка прийматиме 2 аргументи - початок і
кінець діапазона, і вертатиме список простих чисел всередині цього діапазона.'''

def prime_list(start, finish):
    result = []
    for i in range(start, finish + 1):
        exam = 2
        while i % exam != 0:
            exam += 1
        if exam == i:
            result.append(exam)
        else:
            continue
    return result


print(prime_list(15, 150))
