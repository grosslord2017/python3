'''The script to convert decimal to hexadecimal'''


numbers = input().split(', ')

bufer_list = []

for number in numbers:
    numb = str(hex(int(number)))[2:]
    if len(numb) < 2:
        numb = '0' + numb
        bufer_list.append(numb)
    else:
        bufer_list.append(numb)

print(' '.join(bufer_list))
