DATA_BASE = 'db.txt'
import os


class Book:
    def __init__(self, book_id, title, author, year, status="в наличии"):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return (f'ID: {self.id}, Название: "{self.title}",
                Автор: {self.author}, Год: {self.year},
                Статус: {self.status}'
                )


def add_book(title: str, author: str, year: int) -> None:
    '''Добавление книги в базу.'''

    books = load_books()
    print(books)
    if len(books) == 0:
        book_id = 1
    else:
        book_id = books[-1].id + 1
    new_book = Book(book_id, title, author, year)
    books.append(new_book)
    save_books(books)
    print(f'Книга "{title}" добавлена в библиотеку.')

def delete_book(book_id: int) -> None:
    '''Удаление книги в базу.'''

    books = load_books()
    for book in books:
        if book.id == book_id:
            books.remove(book)
            save_books(books)
            print(f'Книга с ID {book_id} удалена из библиотеки.')
            return
    print(f'Книга с ID {book_id} не найдена.')

def search_books(find_request: str) -> tuple:
    '''Поиск книг по запросу.'''

    books = load_books()
    results = []
    for book in books:
        if (find_request.lower() in book.title.lower()
            or find_request.lower() in book.author.lower()
            or find_request == str(book.year)):
            results.append(book)
    return results

def change_status(book_id: int, new_status: str) -> None:
    '''Изменение статуса книги.'''

    books = load_books()
    if new_status not in ['в наличии', 'выдана', '1', '0']:
        print("Некорректный статус. Доступные статусы: 'в наличии', 'выдана', '1', '0'.")
        return
    if new_status in ['в наличии', '1']:
        new_status = 'в наличии'
    if new_status in ['выдана', '0']:
        new_status = 'выдана'
    for book in books:
        if book.id == book_id:
            book.status = new_status
            save_books(books)
            print(f'Статус книги с ID {book_id} изменен на "{new_status}".')
            return
    print(f'Книга с ID {book_id} не найдена.')

def load_books() -> tuple:
    '''Загрузка всех книг в память.'''

    books = []
    if os.path.exists(DATA_BASE):
        with open(DATA_BASE, 'r', encoding='utf-8') as file:
            for line in file:
                book_id, title, author, year, status = line.strip().split('|')
                books.append(Book(int(book_id), title, author, int(year), status))
    return books

def save_books(books: tuple) -> None:
    '''Сохраниение всех книг из памяти в файл.'''

    with open(DATA_BASE, 'w', encoding='utf-8') as file:
        for book in books:
            file.write(f'{book.id}|{book.title}|
                       {book.author}|{book.year}|{book.status}\n'
                       )

def main():
    '''Главное меню.'''

    while True:
        command_from_user = input(
            '\n1. Добавить книгу (add),\n2. Удалить книгу (del),'
            '\n3. Поиск книги (find),\n4. Показать все книги (ls),'
            '\n5. Изменить статус книги (ch)'
            '\nВыберите действие цифрой, командой или текстом: ')
        if command_from_user in ['add', 'Add', 'ADd', 'ADD', 
                                 'Добавить книгу','добавить книгу', '1'
                                 ]:
            try:
                title = input('Введите название книги: ')
                author = input('Введите автора: ')
                year = int(input('Введите год издания: '))
                add_book(title, author, year)
            except ValueError:
                print('Год издания должен состоять только из цифр')
        if command_from_user in ['del', 'DEl', 'DEL', 'Удалить книгу',
                                 'удалить книгу', '2'
                                 ]:
            try:
                id = int(input('Укажите ID книги: '))
                delete_book(id)
            except ValueError:
                print('ID введен не корректно, попробуйте еще раз')
        if command_from_user in ['find', 'Find', 'FInd', 'FINd', 'FIND', 'Поиск книги', 'поиск книги', '3']:
            find_request = input("Введите название, автора или год для поиска: ")
            results = search_books(find_request)
            if results:
                print("Результаты поиска:")
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.")
        if command_from_user in ['ls', 'Ls', 'LS', 'Показать все книги',
                                 'показать все книги', '4'
                                 ]:
            books = load_books()
            if books:
                for book in books:
                    print(book)
            else:
                print('Библиотека пуста')
        if command_from_user in ['ch', 'Ch', 'CH', 'Изменить статус книги', 'изменить статус книги', '5']:
            try:
                book_id = int(input("Введите ID книги для изменения статуса: "))
                new_status = input('Введите новый статус цифрой или текстом - в наличии (1) или выдана (0): ')
                change_status(book_id, new_status)
            except ValueError:
                print('ID введен не корректно, попробуйте еще раз')


if __name__ == "__main__":
    main()
