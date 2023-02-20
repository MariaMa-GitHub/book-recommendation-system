"""
System Class
"""
import pandas

from book import Book


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
