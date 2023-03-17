"""
System Class
"""
import pandas

from book import Book
from author import load_author_data
from genre import extract_genre

import csv


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
        self.load_book_genres()

    def load_book_authors(self):
        """
        Load book author
        """

        data = load_author_data()

        for id in self.books:

            book = self.books[id]

            for author in book.authors:

                if author in data:
                    book.authors[author] = data[author]

    def load_book_genres(self):
        """
        Load book author
        """

        for id in self.books:

            book = self.books[id]

            book.genres = extract_genre(book.link)
            print(book.genres)
            print(book.link)

        # with open('genres.csv', 'w', newline='') as file:
        #
        #     w = csv.writer(file, quoting=csv.QUOTE_ALL)
        #
        #     for id in self.books:
        #
        #         book = self.books[id]
        #
        #         book.genres = extract_genre(book.link)
        #
        #         w.writerow([str(id)] + book.genres)
