'''Запишіть в один рядок генератор списку (числа в діапазоні від 0 до 100),
сума цифр кожного елемент якого буде дорівнювати 10.
Перевірка: [19, 28, 37, 46, 55, 64, 73, 82, 91]'''

test_list = [number for number in range(101) if sum([int(i) for i in str(number)]) == 10]

print(test_list)