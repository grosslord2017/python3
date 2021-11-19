''' Написати скрипт, який пройдеться по списку, який складається із кортежів,
і замінить для кожного кортежа останнє значення.
Значення, на яке замінюється останній елемент кортежа вводиться користувачем.
Кортежи вводить в формате n, n1, n2 ... '''

#Блок для ввода кортежей и добавление их в один список
list_of_tuples = []
while True:
    new_taple_string = input('Введите кортеж или пустую строку для завершения ввода: ').split(', ')
    if new_taple_string == ['']:
        break
    else:
        new_tuple_list = [int(x) for x in new_taple_string]
        list_of_tuples.append(tuple(new_tuple_list))

#Блок для замены последних элементов кортежей в списке на число, которое мы введем (variable)
variable = int(input("число, на которое будем менять последний элемент: "))
result = []
for i in list_of_tuples:
    i = list(i)
    i[-1] = variable
    i = tuple(i)
    result.append(i)
print(result)
