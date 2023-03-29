"""If the given user has no past reading records stores in the manager system OR the user
with an existing account wants to explore books whose genres are not contained in this
user's past reading activities, use this decision-tree-based recommendation system (called
a recommendation system) to make recommendations.
"""
from __future__ import annotations
from typing import Any
from book import Book
# from python_ta.contracts import check_contracts

SYSTEM_START = '*'
MATCH_SCORE = 7


# @check_contracts
class RecommendationSystem:
    """A recommendation system based on the decision tree. This system is used when
    either the user has no account recorded or the user wants to explore books of genres
    which haven't appeared in this user's past reading activities.
    """
    item: Any
    subsystems: dict[Any, RecommendationSystem]

    def __init__(self, books: dict[int, Book], root: Any = SYSTEM_START) -> None:
        """Initialize this recommendation system."""
        self.item = root
        self.subsystems = {}
        self.books = books

    def add_subsystem(self, subsystem: RecommendationSystem) -> None:
        """Add subsystem to this recommendation system."""
        self.subsystems[subsystem.item] = subsystem

    def insert_attributes(self, book_attributes: list) -> None:
        """Insert book_attributes into this recommendation system such that every next
        entry in book_attributes is a child of the current one.
        """
        self._insert_attributes_util(book_attributes, 0)

    def _insert_attributes_util(self, book_attributes: list, start: int) -> None:
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
                attributes_copy = attributes[:4] + [author_id] + attributes[5:]
                self.insert_attributes(attributes_copy)

    def recommend(self, responses: list) -> set[int]:
        """Return a set of IDs of the recommended books based on the responses to a series
        of questions provided by the user.

        Preconditions:
            - len(responses) == 8
        """
        possible_recommended = self._recommend_util(responses, 0)

        for i in range(len(possible_recommended) - 1, -1, -1):
            book_attributes = self.books[possible_recommended[i]].get_attributes()
            if _get_match_score(book_attributes, responses) < MATCH_SCORE:
                possible_recommended.pop(i)

        return set(possible_recommended)

    def _recommend_util(self, responses: list, start: int) -> list[int]:
        """A helper method for RecommendationSystem.recommend."""
        if start == len(responses):
            return list(self.subsystems[subsystem].item for subsystem in self.subsystems)

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

    # def height(self) -> int:
    #     if self.subsystems == {}:
    #         return 1
    #     else:
    #         return 1 + max(self.subsystems[subsystem].height() for subsystem in self.subsystems)
    #
    # def num_leaves(self) -> int:
    #     if self.subsystems == {}:
    #         return 1
    #     else:
    #         counter = 0
    #         for subsystem in self.subsystems:
    #             counter += self.subsystems[subsystem].num_leaves()
    #         return counter
    #
    # def str_rep(self, depth: int) -> str:
    #     if self.subsystems == {}:
    #         if self.item == '*':
    #             return '*'
    #         else:
    #             return ' ' * depth + str(self.item)
    #     else:
    #         result = ' ' * depth + f'{self.item}\n'
    #         for sub in self.subsystems:
    #             curr_sub = self.subsystems[sub]
    #             result += curr_sub.str_rep(depth + 1)
    #         return result
    #
    # def __str__(self) -> str:
    #     return self.str_rep(0)


def _get_match_score(attributes: list, responses: list) -> int:
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
        - isinstance(responses[0], tuple)
    """
    total = 0

    for i in range(len(responses)):
        if i == 0 and responses[i][0] <= attributes[i] <= responses[i][1]:
            total += 1
        elif i > 0 and attributes[i] == responses[i]:
            total += 1

    return total


if __name__ == '__main__':
    # rec_sys = RecommendationSystem()
    # rec_sys.initialize()
    # print(rec_sys.recommend([(100, 500), 'US', 'eng', '', [50873, 232533], '', '']))
    pass
