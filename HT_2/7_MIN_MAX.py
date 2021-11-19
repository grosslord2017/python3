'''Написати скрипт, який отримає максимальне і мінімальне
значення із словника. Дані захардкодити.'''

dict_1 = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60}

val_list = dict_1.values()
max_v = max(dict_1.values())
min_v = min(dict_1.values())

print(f"MAXIMUM -> {max_v}")
print(f"MINIMUM -> {min_v}")
