'''The script to check whether a specified value is
contained in a group of values.'''

number = int(input("Enter the number to search: "))
array = set(input("Enter the array: " ).split(', '))
group = []

for g in group:
    g = int(g)
    group.append(g)

find = number in group

print(f"{number} -> {group} : {find}")
#print(f"{number} -> {tuple(group)} : {find}")
