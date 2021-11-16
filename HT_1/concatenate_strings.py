'''Еhe script accepts lines until the user enters 'q' or 'Q', after which all entered lines will be concatenated'''

list_of_strings = []

while True:
    print("Enter the string or enter 'q' to exit: ")
    row = input()
    if row == 'q' or row == 'Q':
        break
    else:
        list_of_strings.append(row)

concat_strings = ' '.join(list_of_strings)
print(concat_strings)
