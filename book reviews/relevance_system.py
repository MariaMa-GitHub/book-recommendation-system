"""If the given user already has reading records stored in the manager system, then
use this graph-based recommendation system (called a relevance system) to make
further recomendations.
"""
from __future__ import annotations
from recommendation_system import LIBRARY


RELEVANCE_FACTOR = 50


class _BookVertex:
    book_id: int  # book_id
    similar_books: set[_BookVertex]  # ids of similar books

    def __init__(self, book_id: int, similar_books: set[_BookVertex]) -> None:
        self.book_id = book_id
        self.similar_books = similar_books


class BookGraph:
    """..."""
    books: dict[int, _BookVertex]

    def __init__(self) -> None:
        """..."""
        self.books = {}

    def __contains__(self, book_id: int) -> bool:
        """Return whether book_id is in self.vertices."""
        return book_id in self.books

    def add_vertex(self, book_id: int) -> None:
        """TODO: ...

        Preconditions:
            - book_id not in self.book_ids
        """
        self.books[book_id] = _BookVertex(book_id, set())

    def add_edge(self, book_id1: int, book_id2: int) -> None:
        """TODO: ..."""
        if book_id1 not in self.books:
            self.add_vertex(book_id1)

        if book_id2 not in self.books:
            self.add_vertex(book_id2)

        book1 = self.books[book_id1]
        book2 = self.books[book_id2]
        book1.similar_books.add(book2)
        book2.similar_books.add(book1)

    def __str__(self) -> str:
        str_rep = ''
        for book in self.books:
            similar_books = [book.book_id for book in self.books[book].similar_books]
            str_rep += f'{book}: {similar_books}\n'

        return str_rep


class SimilarBookSystem:
    """..."""
    book_graph: BookGraph

    def __init__(self) -> None:
        """..."""
        self.book_graph = BookGraph()

    def initialize(self) -> None:
        """Initialize this similar book system.

        Preconditions:
            - self is empty an empty graph
        """
        for book_id in LIBRARY:
            self.book_graph.add_vertex(book_id)
            similar_books = LIBRARY[book_id].similar_books
            for similar_book_id in similar_books:
                self.book_graph.add_vertex(similar_book_id)
                self.book_graph.add_edge(book_id, similar_book_id)

    def recommend(self, books: set[int]) -> set[int]:  # books: a list of book IDs
        """TODO: ..."""
        counter = {}
        similar_books = set()

        for book_id in books:
            similar_books.update(LIBRARY[book_id].similar_books)

        for book_id in similar_books:
            for lib_book in LIBRARY:
                if book_id in LIBRARY[lib_book].similar_books:
                    if book_id not in counter:
                        counter[book_id] = 1
                    else:
                        counter[book_id] += 1

        counter = list(counter.items())
        counter.sort(reverse=True, key=lambda tup: tup[1])

        return {book_id for book_id, book_freq in counter if book_freq >= RELEVANCE_FACTOR}


if __name__ == '__main__':
    sbs = SimilarBookSystem()
    sbs.initialize()
    # print(len(sbs.recommend({12260608, 19500293, 21839887, 22642971, 16028447, 18736678, 26385201, 13576500, 24809790,
    #                          13533758, 18651847, 25782731, 20549965, 30163661, 7263842, 17065958, 27826791, 16128108,
    #                          34927215, 7989237, 19033466, 15713917})))
