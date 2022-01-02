'''Створити клас Person, в якому буде присутнім метод __init__ який буде приймати * аргументів,
які зберігатиме в відповідні змінні. Методи, які повинні бути в класі Person - show_age, print_name,
show_all_information.
   - Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атребут profession.
'''

class Person(object):

    __doc__ = 'class initialization new person. He takes 5 arguments: Name, age, gender, growth, weight.'

    def __init__(self, name, age, gender, growth, weight):
        self.name = name
        self.age = age
        self.gender = gender
        self.growth = growth
        self.weight = weight

    def show_age(self):
        print(self.age)

    def print_name(self):
        print(self.name)

    def show_all_information(self):
        print("Gender:".ljust(10) + f"{self.gender}")
        print("Name:".ljust(10) + f"{self.name}")
        print("Age:".ljust(10) + f"{self.age}")
        print("Growth:".ljust(10) + f"{self.growth}")
        print("Weight:".ljust(10) + f"{self.weight}")


obj_1 = Person('Valera', 25, 'male', 85, 190)
obj_2 = Person('Alina', 30, 'female', 55, 185)

obj_1.proffesion = 'Lawyer'
obj_2.proffesion = 'Proffesor'

obj_2.show_all_information()
print(obj_2.proffesion)