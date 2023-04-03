"""CSC111 Winter 2023 Course Project: Book Recommendation System

Descriptions and Instructions
===============================
This module contains a customized class called Book that is used
to represent a book.

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


class Book:
    """A Book class that contains the metadata of a book.

    Instance Attributes:
        - book_id: book id
        - title: book title
        - is_ebook: whether this book has an e-book version
        - authors: a mapping of author id to author name, represeting the author(s) of the book
        - publisher: book publisher
        - publication_year: publication year of the book
        - country: book's country of origin
        - language: language in which the book is written
        - num_pages: number of pages of the book
        - genres: a list of the genres of the book
        - average_rating: the average of book's ratings
        - ratings_count: the number of book's ratings
        - description: description of the book
        - similar_books: a set of similar books' ids
        - link: Goodreads url of the book
    """
    book_id: int
    title: str
    is_ebook: bool
    authors: dict[int, str]
    publisher: str
    publication_year: int
    country: str
    language: str
    num_pages: int
    genres: set[str]
    average_rating: float
    ratings_count: int
    description: str
    similar_books: set[int]
    link: str

    def __init__(self, df: pandas.DataFrame, i: int) -> None:
        """Initialize book info using books dataframe."""
        self.book_id = int(df.iloc[i]['book_id'])
        self.title = df.iloc[i]['title']
        self.is_ebook = bool(df.iloc[i]['is_ebook'])
        self.authors = {int(author['author_id']): '' for author in df.iloc[i]['authors']}
        self.publisher = df.iloc[i]['publisher']
        self.publication_year = int(df.iloc[i]['publication_year'])
        self.country = df.iloc[i]['country_code']
        self.language = df.iloc[i]['language_code']
        self.num_pages = int(df.iloc[i]['num_pages'])
        self.genres = {shelf['name'] for shelf in df.iloc[i]['popular_shelves'] if int(shelf['count']) >= 10}
        self.average_rating = float(df.iloc[i]['average_rating'])
        self.ratings_count = int(df.iloc[i]['ratings_count'])
        self.description = df.iloc[i]['description']
        self.similar_books = {int(book_id) for book_id in df.iloc[i]['similar_books']}
        self.link = df.iloc[i]['link']

    def get_attributes(self) -> tuple:
        """Return a tuple of attributes that are used in the tree-based recommendation system."""
        return (self.num_pages, self.country, self.language,
                self.title, frozenset(self.authors.keys()), self.publisher, self.publication_year,
                self.is_ebook, self.book_id)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['pandas'],
        'disable': ['too-many-instance-attributes']
    })
