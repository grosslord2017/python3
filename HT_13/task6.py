'''Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.'''

class Person(object):

    count = 0

    def __init__(self, name, age):
        Person.count += 1
        self.name = name
        self.age = age


obj1 = Person('Valera', 25)
print(Person.count)

obj2 = Person('Alina', 30)
print(Person.count)