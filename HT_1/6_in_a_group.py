'''The script to check whether a specified value is
contained in a group of values.'''

number = int(input("Enter the number to search: "))
array = input("Enter numbers where to search: " ).split(', ')

group = [int(x) for x in array]
find = number in group

print(f"{number} -> {group} : {find}")
#print(f"{number} -> {tuple(group)} : {find}")
