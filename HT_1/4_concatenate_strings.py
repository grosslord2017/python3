'''Еhe script accepts lines until the user enters 'q' or 'Q', after which all entered lines will be concatenated'''

number_strings = int(input("Enter number of strings: "))
count = 0
list_of_strings = []

while number_strings > count:
    row = input("Enter a string: ")
    list_of_strings.append(row)
    count += 1

print(''.join(list_of_strings))
