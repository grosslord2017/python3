'''Script to sum of the first n positive integers'''

number = int(input('Enter a natural number: '))
sum = 0

for iter in range(number + 1):
    sum += iter

print(sum)
