'''Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки(включіть фантазію).'''

class Book(object):

    def __init__(self, author, book_name, year):
        self.author = author
        self.book_name = book_name
        self.year = year

    def __str__(self):
        return f"{self.book_name}; {self.author}; {self.year}"


class Library(object):

    list_of_books = []

    def add_book(self, book):
        Library.list_of_books.append(book)
        Library.list_of_books.sort()

    def show_book_list(self):
        for book in Library.list_of_books:
            print(book)

    def take_a_book(self, book_name):
        name = []
        if not Library.list_of_books:
            print("Sorry, but I can't give out the book")
        else:
            for book in Library.list_of_books:
                info_book = book.split('; ')
                if book_name in info_book[0]:
                    name.append(book)
                else:
                    continue

            if not name:
                print('There is no such book')
                print('-' * 30)
            else:
                Library.list_of_books.remove(name[0])

    def find_all_books(self, word):
        for book in Library.list_of_books:
            if word in book:
                print(book)
            else:
                continue



def initialization():
    lib = Library()
    start_books = [['J.K.Rowling', 'Harry Potter', 1997], ['J.R.R.Tolkien', 'The Lord of the Rings', 1990], ['C.S.Lewis', 'The Chronicles of Narnia', 1950]]
    for i in start_books:
        book = Book(i[0], i[1], str(i[2]))
        lib.add_book(str(book))

def menu():
    lib = Library()
    print('1 - show a list of available books')
    print('2 - add book in library')
    print('3 - take a book')
    print('4 - find all books by keyword ')
    print('5 - exit')
    choice = input('Your choice: ')
    if choice == '1':
        print('-' * 30)
        lib.show_book_list()
        print('-' * 30)
    elif choice == '2':
        print('Enter the author, title and year of the book')
        print('Example: author; title; year')
        new_book = input('New book: ').split('; ')
        book = Book(new_book[0], new_book[1], new_book[2])
        lib.add_book(str(book))
        print('-' * 30)
    elif choice == '3':
        print('What book do you want to take?')
        book_name = input('Book title: ')
        lib.take_a_book(book_name)
        print('-' * 30)
    elif choice == '4':
        word = input('keyword: ')
        lib.find_all_books(word)
        print('-' * 30)
    elif choice == '5':
        exit()
    else:
        print('No such choice')
        print('-' * 30)



initialization()
while True:
    menu()





