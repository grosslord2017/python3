'''Створити цикл від 0 до ... (вводиться користувачем).
В циклі створити умову, яка буде виводити поточне значення,
якщо остача від ділення на 17 дорівнює 0.'''

number = int(input('Enter number: '))

for numb in range(number + 1):
    if numb % 17 == 0 and numb != 0:
        print(numb)
    else:
        continue