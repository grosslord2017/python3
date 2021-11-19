'''Написати скрипт, який отримує від користувача позитивне ціле число
і створює словник, з ключами від 0 до введеного числа, а значення
для цих ключів - це квадрат ключа'''

number = int(input("Enter a number: "))
numbers = [x for x in range(0, number + 1)]

dict1 = {}
for numb in numbers:
    dict1[numb] = numb * numb

print(dict1)
