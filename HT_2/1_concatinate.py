'''Написати скрипт, який конкатенує всі елементи в списку і виведе їх на екран.'''

hard = [1, 2, 'test', 10, 'foo', 15, 'egg', 'hello']

#Вариант с "плюсованием" строк
temp = ''
for i in hard:
    temp += str(i)

print(temp)

#Вариант с методом join
temp = []
for i in hard:
    temp.append(str(i))

print(''.join(temp))

#Вариант с пользовательским вводом
# number_strings = int(input("Enter number of strings: "))
# count = 0
# list_of_strings = []
#
# while number_strings > count:
#     row = input("Enter a string: ")
#     list_of_strings.append(row)
#     count += 1
#
# print(''.join(list_of_strings))
