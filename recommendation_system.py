"""CSC111 Winter 2023 Course Project: Book Recommendation System

Descriptions and Instructions
===============================
This module contains the main algorithms with which book recommendations
are made. Specifically, this module contains the recommendation algorithm
used for recommending books based on the user's preferences as well as the
one used for finding books that are similar to the ones saved by the user.

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
from __future__ import annotations
from typing import Any
import random
from book import Book


SYSTEM_START = '*'
RELEVANCE_FACTOR = 50


##################################################################
#          Recommendation System for Finding New Books           #
##################################################################
class RecommendationSystem:
    """A recommendation system based on the decision tree. This system is used when
    either the user has no account recorded or the user wants to explore books of genres
    which haven't appeared in this user's past reading activities.
    """
    item: Any
    subsystems: dict[Any, RecommendationSystem]
    books: dict[int, Book]

    def __init__(self, books: dict[int, Book], root: Any = SYSTEM_START) -> None:
        """Initialize this recommendation system."""
        self.item = root
        self.subsystems = {}
        self.books = books

    def add_subsystem(self, subsystem: RecommendationSystem) -> None:
        """Add subsystem to this recommendation system."""
        self.subsystems[subsystem.item] = subsystem

    def insert_attributes(self, book_attributes: tuple) -> None:
        """Insert book_attributes into this recommendation system such that every next
        entry in book_attributes is a child of the current one.
        """
        self._insert_attributes_util(book_attributes, 0)

    def _insert_attributes_util(self, book_attributes: tuple, start: int) -> None:
        """A helper method for RecommendationSystem.insert_attributes."""
        if start != len(book_attributes):
            if book_attributes[start] not in self.subsystems:
                self.add_subsystem(RecommendationSystem(self.books, book_attributes[start]))
            self.subsystems[book_attributes[start]]._insert_attributes_util(book_attributes, start + 1)

    def initialize(self) -> None:
        """Initialize this recommendation system. At the beginning, this system is emtpy
        and needs to be initialized with a collection of books.

        Preconditions:
            - self.item == SYSTEM_START
            - self.subsystems == {}
        """
        for book_id in self.books:
            attributes = self.books[book_id].get_attributes()
            authors = attributes[4]
            for author_id in authors:
                attributes_copy = attributes[:4] + tuple([author_id]) + attributes[5:]
                self.insert_attributes(attributes_copy)

    def recommend(self, responses: list) -> set[int]:
        """Return a set of IDs of the recommended books based on the responses to a series
        of questions provided by the user.

        Preconditions:
            - len(responses) == 8
        """
        possible_recommended = self._recommend_util(responses, 0)
        max_match = max(
            possible_recommended,
            key=lambda x: _get_match_score(self.books[x].get_attributes(), responses)
        )

        recommended = []
        for book in possible_recommended:
            curr_match_score = _get_match_score(self.books[book].get_attributes(), responses)
            max_match_score = _get_match_score(self.books[max_match].get_attributes(), responses)
            if curr_match_score == max_match_score:
                recommended.append(book)

        if len(recommended) > 60:
            return set(random.sample(recommended, 60))
        else:
            return set(recommended)

    def _recommend_util(self, responses: list, start: int) -> list[int]:
        """A helper method for RecommendationSystem.recommend."""
        if start == len(responses):
            return list(self.subsystems[key].item for key in self.subsystems)

        all_recommended = []
        attribute = responses[start]
        found = False
        if start == 0:
            min_pages, max_pages = attribute
            for subsystem in self.subsystems:
                if min_pages <= self.subsystems[subsystem].item <= max_pages:
                    found = True
                    all_recommended.extend(self.subsystems[subsystem]._recommend_util(responses, start + 1))
        else:
            for subsystem in self.subsystems:
                if attribute == self.subsystems[subsystem].item:
                    found = True
                    all_recommended.extend(self.subsystems[subsystem]._recommend_util(responses, start + 1))

        if not found:
            for subsystem in self.subsystems:
                all_recommended.extend(self.subsystems[subsystem]._recommend_util(responses, start + 1))

        return all_recommended


def _get_match_score(attributes: tuple, responses: list) -> int:
    """Return the match score between attributes and responses.

    Let attributes be the list of attributes of a given book defined in the method
    Book.get_attributes and let responses be the user's reading preference. Let i be an integer
    such that 0 <= i < min(len(attributes), len(responses)). Then we say responses[i] and
    attributes[i] are matching entries if one of the following cases follows:

        - i == 0 and responses[i][0] <= attributes[i] <= responses[i][1]
        - i > 0 and responses[i] == attributes[i]

    We define the match score between attributes and responses be the number of matching
    entries between these two lists.

    Preconditions:
        - len(attributes) == 9
        - len(responses) == 8
    """
    total = 0

    for i in range(len(responses)):
        if i == 0 and responses[i][0] <= attributes[i] <= responses[i][1]:
            total += 10
        elif 0 < i < 3 and any(response == attributes[i] for response in responses[i]):
            total += 10
        elif (i == 3 and responses[i] == attributes[i]) or (i > 4 and responses[i] == attributes[i]):
            total += 1
        elif i == 4 and any(author == responses[i] for author in attributes[i]):
            total += 1

    return total


#################################################################
#            Recommendation System for Similar Books            #
#################################################################
class _BookVertex:
    """A _BookVertex class that represents a book in a graph.

    Instance Attributes:
        - book_id: the ID of this book
        - similar_books: the IDs of books that are similar to this book

    Representation Invariants:
        - all(book.book_id != self.book_id for book in self.similar_books)
    """
    book_id: int  # book_id
    similar_books: set[_BookVertex]

    def __init__(self, book_id: int, similar_books: set[_BookVertex]) -> None:
        """Initialize this book vertex."""
        self.book_id = book_id
        self.similar_books = similar_books


class BookGraph:
    """A BookGraph that represents a graph of books. Specifically, every book in
    this graph is connected to another book that is similar to itself.
    """
    books: dict[int, _BookVertex]

    def __init__(self) -> None:
        """..."""
        self.books = {}

    def __contains__(self, book_id: int) -> bool:
        """Return whether book_id is in self.vertices."""
        return book_id in self.books

    def add_book(self, book_id: int) -> None:
        """Add the book with book_id to this book graph.

        Preconditions:
            - book_id not in self.book_ids
        """
        self.books[book_id] = _BookVertex(book_id, set())

    def connect_books(self, book_id1: int, book_id2: int) -> None:
        """Connect books with book_id1 and book_id2 with an edge in this book graph.
        If either of those books are not presented in the graph, then first add it
        to this graph and then connect them together.

        Preconditions:
            - book_id1 != book_id2
        """
        if book_id1 not in self.books:
            self.add_book(book_id1)

        if book_id2 not in self.books:
            self.add_book(book_id2)

        book1 = self.books[book_id1]
        book2 = self.books[book_id2]
        book1.similar_books.add(book2)
        book2.similar_books.add(book1)


class SimilarBookSystem:
    """A SimilarBookSystem class that represents a recommendation system that searches
    for similar books.

    Books that are similar to each other are connected by an edge in this system's book
    graph.

    Instance Attributes:
        - book_graph: a book graph in this system that connects each pair of similar books
        - books: a dictionary that maps each book's ID to the corresponding Book object
    """
    book_graph: BookGraph
    books: dict[int, Book]

    def __init__(self, books: dict[int, Book]) -> None:
        """..."""
        self.book_graph = BookGraph()
        self.books = books

    def initialize(self) -> None:
        """Initialize this similar book system.

        Preconditions:
            - self is empty an empty graph
        """
        for book_id in self.books:
            self.book_graph.add_book(book_id)
            similar_books = self.books[book_id].similar_books
            for similar_book_id in similar_books:
                self.book_graph.add_book(similar_book_id)
                self.book_graph.connect_books(book_id, similar_book_id)

    def recommend(self, books: set[int]) -> set[int]:
        """Return a set of IDs of books that are similar to those in books.
        Every book in the returned set cannot appear in books.
        """
        counter = {}
        similar_books = set()

        for book_id in books:
            similar_books.update(self.books[book_id].similar_books)

        for book_id in similar_books:
            for lib_book in self.books:
                if book_id in self.books[lib_book].similar_books:
                    if book_id not in counter:
                        counter[book_id] = 1
                    else:
                        counter[book_id] += 1

        counter = list(counter.items())
        counter.sort(reverse=True, key=lambda tup: tup[1])

        return {book for book, book_freq in counter
                if book_freq >= RELEVANCE_FACTOR and book not in books}


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['__future__', 'typing', 'book', 'random'],
        'disable': ['too-many-nested-blocks']
    })
