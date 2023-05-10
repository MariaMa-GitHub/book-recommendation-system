"""CSC111 Winter 2023 Course Project: Book Recommendation System

Descriptions and Instructions
===============================
This module contains a customized class called Library that is used
to represent a system containing all the books and allowing user
interactions.

Copyright and Usage Information
===============================
This file is provided solely for the usage of this project's authors
and the grading purpose of the instructors and teaching assistants
from CSC111 at the University of Toronto, St. George campus. The
authors of this code retain all rights to the code contained within
this file. All forms of distribution of this code, regardless of
changes, are expressly prohibited. For more information on copyright
for CSC111 project materials, please consult the Course Syllabus
for CSC111, Winter 2023.

This file is Copyright (c) 2023 Jayden Chiola-Nakai, Maria Ma,
Kaiwen Zheng, and Shaqeel Hazmi Bin Radzifuddin
"""

import pandas
from book import Book
from author import load_author_data
from genre import filter_genres


class Library:
    """A class that represents a system containing all the books and allowing user interactions.

    Instance Attributes:
        - books: a mapping from book id to the corresponding book, representing a repository of books
    """
    books: dict[int, Book]

    def __init__(self) -> None:
        """Initialize the library."""
        self.books = {}

    def load_books(self, df: pandas.DataFrame) -> None:
        """Load books into the system given the books dataframe."""
        for i in range(len(df.index)):
            book = Book(df, i)
            self.books[book.book_id] = book

        self.load_book_authors()
        self.load_book_genres()

    def load_book_authors(self) -> None:
        """Load book author for every book in the library."""
        data = load_author_data()

        for book_id in self.books:
            book = self.books[book_id]
            for author in book.authors:
                if author in data:
                    book.authors[author] = data[author]

    def load_book_genres(self) -> None:
        """Load book genre for every book in the library."""
        for book_id in self.books:
            book = self.books[book_id]
            book.genres = filter_genres(book.genres)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['pandas', 'book', 'author', 'genre']
    })
