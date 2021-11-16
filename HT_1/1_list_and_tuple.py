'''Script which accepts a sequence of comma-separated numbers from user and generate a list and a tuple with those numbers.'''

subsequence = input().split()

new_list = list(subsequence)
new_tuple = tuple(subsequence)

print(f"List: {new_list}")
print(f"Tuple: {new_tuple}")
