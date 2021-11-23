'''Маємо рядок -->
"f98neroi4nr0c3n30irn03ien3c0rfekdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p465jnpoj35po6j345" ->
просто потицяв по клавi. Створіть ф-цiю, яка буде отримувати рядки на зразок цього, яка оброблює наступні випадки:
-  якщо довжина рядка в діапазонi 30-50 -> прiнтує довжину, кiлькiсть букв та цифр
-  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр (лише з буквами)
-  якщо довжина бульше 50 - > ваша фантазiя'''

def processing(line):
    if 30 <= len(line) <= 50:
        result = {'letter': 0, 'number': 0}
        for i in line:
            if i.isdigit():
                result['number'] += 1
            if i.isalpha():
                result['letter'] += 1
        print(f'длина рядка - {len(line)}, букв: {result["letter"]}, цифр: {result["number"]}')
    elif len(line) < 30:
        numbers = []
        letter = []
        for i in line:
            if i.isalpha():
                letter.append(i)
            elif i.isdigit():
                numbers.append(int(i))
        print(f'Сумма чисел - {sum(numbers)}')
        print(f'строка - {"".join(letter)}')
    elif len(line) > 50:
        print(f'Поздравляем, длина строки {len(line)}, и не лень было столько набирать?')




line_string = input('Enter something string: ')
processing(line_string)