'''Програма-світлофор.
Створити програму-емулятор світлофора для авто і пішоходів.
Після запуска програми на екран виводиться в лівій половині - колір автомобільного, а в правій -
пішохідного світлофора. Кожну секунду виводиться поточні кольори. Через декілька ітерацій -
відбувається зміна кольорів - логіка така сама як і в звичайних світлофорах.'''

from time import sleep

def out_light(color, man):
    '''Формирует вывод на экран и делает паузу в 3 секунды'''
    print(color.ljust(15) + man)
    sleep(1)

def traffic_light(car, man='Red', count=4):
    '''Имитирует работу светлофора.
    Для изменения количества выводов Green и Red достаточно передать параметр count. Количество выводов Yellow всегда 2,
    из соображэний что он всегда загорается на пару секунд перед переключением основного цвета.'''
    car_color = car
    for color in car_color:
        if color == 'Green':
            man = 'Red'
            for i in range(count):
                out_light(color, man)
        elif color == 'Yellow' and man == 'Red':
            for i in range(2):
                out_light(color, man)
        elif color == 'Red':
            man = 'Green'
            for i in range(count):
                out_light(color, man)
        elif color == 'Yellow' and man == 'Green':
            for i in range(2):
                out_light(color, man)



while True:
    traffic_light(['Green', 'Yellow', 'Red', 'Yellow'])