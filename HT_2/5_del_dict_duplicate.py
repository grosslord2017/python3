'''Написати скрипт, який залишить в словнику тільки пари із
унікальними значеннями (дублікати значень - видалити).
Словник для роботи захардкодити свій.'''


dict1 = {'1': 10, '2': 20,
         '3': 30, '4': 20,
         'a': 30, 'b': 40,
         'c': 21, 'd': 'hello'}

temp = {}

for key, value in dict1.items():
    if value not in temp.values():
        temp[key] = value
    else:
        continue
print(temp)
