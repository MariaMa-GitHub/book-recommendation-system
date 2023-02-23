"""
If the given user already has reading records stored in the manager system, then
use this graph-based recommendation system (called a relevance system) to make
further recomendations.
"""
from __future__ import annotations
from dataclasses import dataclass
from library import book_repo


RELEVANCE_FACTOR = 2
LIBRARY = book_repo


@dataclass
class _BookVertex:
    book_id: str  # book_id
    neighbours: list[_BookVertex]  # ids of similar books


class BookGraph:
    """..."""
    vertices: dict[str, _BookVertex]

    def __init__(self) -> None:
        """..."""
        self.vertices = {}

    def contains(self, book_id: str) -> bool:
        """..."""
        return book_id in self.vertices

    def add_vertex(self, book_id: str) -> None:
        """..."""
        self.vertices[book_id] = _BookVertex(book_id, [])

    def add_edge(self, book_id1: str, book_id2: str) -> None:
        """..."""
        if self.contains(book_id1) and self.contains(book_id2):
            book_vertex1 = self.vertices[book_id1]
            book_vertex2 = self.vertices[book_id2]
            book_vertex1.neighbours.append(book_vertex2)
            book_vertex2.neighbours.append(book_vertex1)
        else:
            raise ValueError


class SimilarBookSystem:
    """..."""
    book_graph: BookGraph

    def __init__(self) -> None:
        """..."""
        self.book_graph = BookGraph()
        for book_id in LIBRARY:
            similar_books = LIBRARY[book_id].similar_books
            if not self.book_graph.contains(book_id):
                self.book_graph.add_vertex(book_id)

            for similar_book_id in similar_books:
                if not self.book_graph.contains(similar_book_id):
                    self.book_graph.add_vertex(similar_book_id)
                self.book_graph.add_edge(book_id, similar_book_id)

    def explore_by_depth(self, start_id: str, d: int) -> list[str]:
        """..."""
        visited = set()
        accumulator = []
        self._explore_by_depth_helper(start_id, d, visited, accumulator)
        return accumulator

    def _explore_by_depth_helper(self, start_id: str, d: int, visited: set[str], accumulator: list[str]) -> None:
        """..."""
        if d == 0 or self.book_graph.vertices[start_id].neighbours == set():
            return
        else:
            visited.add(start_id)
            neighbours = self.book_graph.vertices[start_id].neighbours
            for neighbour in neighbours:
                neighbour_id = neighbour.book_id
                if neighbour_id not in visited:
                    accumulator.append(neighbour_id)
                    self._explore_by_depth_helper(neighbour_id, d - 1, visited, accumulator)

    # def __str__(self) -> str:
    #     """..."""
    #     str_rep = ''
    #     for book_id in self.book_graph.vertices:
    #         str_rep += book_id + ': ['
    #         neighbours = self.book_graph.vertices[book_id].neighbours
    #         for neighbour in neighbours:
    #             str_rep += (neighbour.book_id + ', ')
    #         str_rep += ']\n'
    #     return str_rep


if __name__ == '__main__':
    sbs = SimilarBookSystem()
