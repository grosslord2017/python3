'''Користувачем вводиться початковий і кінцевий рік.
Створити цикл, який виведе всі високосні роки в цьому проміжку (границі включно).
рік кратний 400; рік кратний 4, але не кратний 100'''

year_start = int(input('Enter start year: '))
year_finish = int(input('Enter finish year: '))

for year in range(year_start, year_finish + 1):
    if (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0):
        print(year)
    else:
        continue