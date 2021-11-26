'''Написати функцію, яка приймає на вхід список і підраховує кількість
однакових елементів у ньому.'''

def number_of_idential(arr):
    result = {}
    for i in arr:
        if str(i) not in result.keys():
            result[str(i)] = 1
        else:
            result[str(i)] += 1
    return result

test = number_of_idential([2, 4, 6, 8, 3, 8, 5, 4, 2, 2, 2, 8])
print(test)
