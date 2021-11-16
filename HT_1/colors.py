'''Script to print out a set containing all the
colours from color_list_1 which are not present
in color_list_2.'''

color_list_1 = set(list(input('Enter first set: ').split(', ')))
color_list_2 = set(list(input('Enter second set: ').split(', ')))

print("Result:")
print(color_list_1.difference(color_list_2))
