"""
System Class
"""
import pandas

from book import Book
from author import load_author_data


class Library:
    """
    System containing all the books and allowing user interactions
    """

    books: dict[int, Book]

    def __init__(self):

        self.books = {}

    def load_books(self, df: pandas.DataFrame) -> None:
        """
        Load books into the system
        """

        for i in range(len(df.index)):

            book = Book(df, i)
            self.books[book.id] = book

        self.load_book_authors()

    def load_book_authors(self):
        """
        Load book author
        """

        data = load_author_data()

        for book in self.books:

            for author in self.books[book].authors:

                if author in data:
                    self.books[book].authors[author] = data[author]
