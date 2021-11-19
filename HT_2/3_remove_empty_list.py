'''Написати скрипт, який видалить пусті елементи із списка.
Список можна "захардкодити".'''

hardcod = [(), (), ('',), ('a', 'b'), ('a', 'b', 'c'), ('d')]
final = []
for i in hardcod:
    if bool(i) == False:
        continue
    else:
        final.append(i)

print(final)
