"""If the given user has no past reading records stores in the manager system OR the user
with an existing account wants to explore books whose genres are not contained in this
user's past reading activities, use this decision-tree-based recommendation system (called
a recommendation system) to make recommendations.
"""
from __future__ import annotations
from typing import Any
from main import library


LIBRARY = library.books
SYSTEM_START = '*'


class RecommendationSystem:
    """A recommendation system based on the decision tree. This system is used when
    either the user has no account recorded or the user wants to explore books of genres
    which haven't appeared in this user's past reading activities.
    """
    item: Any
    subsystems: dict[Any, RecommendationSystem]

    def __init__(self, root: Any = SYSTEM_START) -> None:
        """Initialize this recommendation system."""
        self.item = root
        self.subsystems = {}

    def add_subsystem(self, subsystem: RecommendationSystem) -> None:
        """Add subsystem to this recommendation system."""
        self.subsystems[subsystem.item] = subsystem

    def insert_attributes(self, book_attributes: list) -> None:
        """TODO: ..."""
        self._insert_attributes_util(book_attributes, 0)

    def _insert_attributes_util(self, book_attributes: list, start: int) -> None:
        """TODO: ...
        """
        if start != len(book_attributes):
            if book_attributes[start] not in self.subsystems:
                self.add_subsystem(RecommendationSystem(book_attributes[start]))
            self.subsystems[book_attributes[start]]._insert_attributes_util(book_attributes, start + 1)

    def initialize(self) -> None:
        """Initialize this recommendation system. At the beginning, this system is emtpy
        and needs to be initialized with a collection of books.

        Preconditions:
            - self.item == SYSTEM_START
            - self.subsystems == {}
        """
        for book_id in LIBRARY:
            attributes = LIBRARY[book_id].get_attributes()
            authors = attributes[4]
            for author_id in authors:
                attributes_copy = attributes[:4] + [author_id] + attributes[5:]
                self.insert_attributes(attributes_copy)

    def recommend(self, responses: list) -> set[str]:
        """Return a set of IDs of the recommended books based on the responses to a series
        of questions provided by the user.

        Preconditions:
            - len(responses) == 7
        """
        return set(self._recommend_util(responses, 0))

    def _recommend_util(self, responses: list, start: int) -> list[str]:
        """TODO: extract common parts"""
        if start == len(responses):  # have reached one leaf node
            all_recommended = list(self.subsystems.values())
            return [subsystem.item for subsystem in all_recommended]

        if start == 0:
            min_pages, max_pages = responses[start]
            for subsystem in self.subsystems:
                num_pages = self.subsystems[subsystem].item
                if min_pages <= num_pages <= max_pages:
                    return self.subsystems[subsystem]._recommend_util(responses, start + 1)
            else:
                all_recommended = []
                for subsystem in self.subsystems:
                    all_recommended.extend(self.subsystems[subsystem]._recommend_util(responses, start + 1))
                return all_recommended
        else:
            attribute = responses[start]
            for subsystem in self.subsystems:
                if subsystem == attribute:
                    return self.subsystems[subsystem]._recommend_util(responses, start + 1)
            else:
                all_recommended = []
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


if __name__ == '__main__':
    rec_sys = RecommendationSystem()
    rec_sys.initialize()
    print(rec_sys.recommend([(100, 500), 'US', 'eng', '', [50873, 232533], '', '']))
