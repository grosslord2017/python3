'''Напишіть програму, де клас «геометричні фігури» (figure) містить властивість color з початковим
значенням white і метод для зміни кольору фігури, а його підкласи «овал» (oval) і «квадрат» (square) містять
методи __init__ для завдання початкових розмірів об'єктів при їх створенні.

Видозмініть програму так, щоб метод __init__ мався в класі «геометричні фігури» та приймав
кольор фігури при створенні екземпляру, а методи __init__ підкласів доповнювали його та
додавали початкові розміри.'''

class Figure(object):

    def __init__(self, color):
        self.color = color

class Oval(Figure):

    def __init__(self, color, small_axis, major_axis):
        super().__init__(color)
        self.small_axis = small_axis
        self.major_axis = major_axis

class Square(Figure):

    def __init__(self, color, side):
        super().__init__(color)
        self.side = side


obj_1 = Figure('yellow')
obj_2 = Oval('red', 5, 7)
print(obj_2.color)
print(obj_2.small_axis)