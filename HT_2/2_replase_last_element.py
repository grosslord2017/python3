''' Написати скрипт, який пройдеться по списку, який складається із кортежів,
і замінить для кожного кортежа останнє значення.
Значення, на яке замінюється останній елемент кортежа вводиться користувачем.'''

hard = [(10, 20, 40), (40, 50, 60, 70), (80, 90), (1000,)]
variable = int(input("На что будем менять последний элемент: "))
result = []
for i in hard:
    i = list(i)
    i[-1] = variable
    i = tuple(i)
    result.append(i)
print(result)
