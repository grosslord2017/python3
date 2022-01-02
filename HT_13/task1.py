'''Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи повинні виконувати математичні операції з
2-ма числами, а саме додавання, віднімання, множення, ділення.
   - Якщо під час створення екземпляру класу звернутися до атребута last_result він повинен повернути пусте значення
   - Якщо використати один з методів - last_result повенен повернути результат виконання попереднього методу.
   - Додати документування в клас (можете почитати цю статтю: https://realpython.com/documenting-python-code/ )'''

class Calc(object):

    __doc__ = '''This calc has standard function. He takes 2 arguments and save result'''

    last_result = None

    def add(self, a, b):
        '''sums up two arguments'''
        print(Calc.last_result)
        Calc.last_result = a + b

    def subtraction(self, a, b):
        '''subtracting the second argument from first'''
        print(Calc.last_result)
        Calc.last_result = a - b

    def division(self, a, b):
        '''the first argument divides by the second'''
        print(Calc.last_result)
        try:
            Calc.last_result = a / b
        except ZeroDivisionError:
            print('You cannot divide by zero!')

    def mul(self, a, b):
        '''the first argument is multiplied by the second'''
        print(Calc.last_result)
        Calc.last_result = a * b


test = Calc()
print(test.last_result)
print(test.__doc__)

# test.add(5, 10)
# print(test.last_result)

# test.subtraction(5, 4)
# print(test.last_result)

# test.division(7, 0)
# print(test.last_result)

# test.mul(5, 7)
# print(test.last_result)