'''Напишіть програму, де клас «геометричні фігури» (figure) містить властивість color з початковим
значенням white і метод для зміни кольору фігури, а його підкласи «овал» (oval) і «квадрат» (square) містять
методи __init__ для завдання початкових розмірів об'єктів при їх створенні.'''

class Figure(object):

    color = 'white'

    def change_color(self, color):
        Figure.color = color

class Oval(Figure):

    def __init__(self, small_axis, major_axis):
        self.small_axis = small_axis
        self.major_axis = major_axis

class Square(Figure):

    def __init__(self, side):
        self.side = side


obj = Figure()
print(obj.color)

obj.change_color('red')
print(obj.color)

oval = Oval(5, 7)
oval.change_color('green')
print(oval.color)

