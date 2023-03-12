"""
If the given user has no past reading records stores in the manager system OR the user
with an existing account wants to explore books whose genres are not contained in this
user's past reading activities, use this decision-tree-based recommendation system (called
a recommendation system) to make recommendations.
"""
from __future__ import annotations
from typing import Any
import library_kwz


SYSTEM_START = '*'
LIBRARY = library_kwz.book_repo
REVIEW_REPO = library_kwz.review_repo
GENRE_REPO = library_kwz.genre_repo


class RecommendationSystem:
    """A recommendation system based on the decision tree. This system is used when
    either the user has no account recorded or the user wants to explore books of genres
    which haven't appeared in this user's past reading activities.
    """
    item: Any
    subsystems: dict[Any, RecommendationSystem]  # root of recsys --> recsys object

    def __init__(self, root: Any = SYSTEM_START) -> None:
        """Initialize this recommendation system."""
        self.item = root
        self.subsystems = {}

    def add_subsystem(self, subsystem: RecommendationSystem) -> None:
        """TODO: ..."""
        self.subsystems[subsystem.item] = subsystem

    def insert_attributes(self, book_attributes: list) -> None:
        """TODO: ..."""
        self._insert_attributes_util(book_attributes, 0)

    def _insert_attributes_util(self, book_attributes: list[list], start: int) -> None:
        """TODO: ...
        
        Preconditions:
            - all(isinstance(entry, list) for entry in book_attributes)
        """
        if start != len(book_attributes):
            curr_attributes = book_attributes[start]
            for attribute in curr_attributes:
                if attribute not in self.subsystems:
                    self.add_subsystem(RecommendationSystem(attribute))
                self.subsystems[attribute]._insert_attributes_util(book_attributes, start + 1)

    def initialize(self) -> None:
        """TODO: ...
        
        Preconditions:
            - self.item == SYSTEM_START
            - self.subsystems == {}
        """
        for book_id in LIBRARY:
            book = LIBRARY[book_id]
            try:
                book_attributes = [[book._num_pages], GENRE_REPO[book_id], [book._language_code], [book._is_ebook]]
                print(f'len(book_attributes): {len(book_attributes)}')  # TODO: to be deleted...
                self.insert_attributes(book_attributes)
            except KeyError:
                pass    

    # def primary_recommend(self, mandatory_responses: list, start: int) -> list[library_kwz.book]:
    #     """TODO: ...
    #     responses = [page_range (tuple of ints), genre (str), language (str), wants_ebook (bool)]
    #     """
    #     pass

    def recommend(self, responses: list, start: int = 0) -> list[library_kwz.Book]:
        """TODO: ...
        
        responses = [page_range (tuple of ints), genre (str), language (str), wants_ebook (bool),
                    title (optional info, str, case insensitive), author (optional info, author name, str), 
                    publisher (optional info, str, case insensitive), publication_year (optional info, int or None)]
        """
        if start == len(responses):
            return []
        else:
            result = []
            for attribute in self.subsystems:
                if start == 0:
                    if attribute is None or attribute in range(responses[0], responses[1] + 1):  # num_pages attribute
                        result.extend(self.subsystems[attribute].recommend(responses, start + 1))
                else:
                    if attribute == responses[start]:
                        result.extend(self.subsystems[attribute].recommend(responses, start + 1))
            return result   

    def depth(self) -> int:
        if self.subsystems == {}:
            return 1
        else:
            return 1 + max(self.subsystems[s].depth() for s in self.subsystems)            

    def __len__(self) -> int:
        if self.subsystems == {}:
            return 1
        else:
            return 1 + sum(self.subsystems[s].__len__() for s in self.subsystems)     


# def initialize_system(empty_system: RecommendationSystem) -> None:
#     """Initialize the recommendation system

#     Preconditions:
#         - empty_system.item == SYSTEM_START
#     """
#     for book_id in LIBRARY:
#         if book_id in GENRE_REPO:
#             book = LIBRARY[book_id]
#             book_attributes = [[book._num_pages], GENRE_REPO[book_id], [book._language_code], [book._is_ebook]]
#             empty_system.insert_attributes(book_attributes)
    

if __name__ == '__main__':
    # rec_sys = RecommendationSystem()
    # initialize_system(rec_sys)
    # print(len(rec_sys.subsystems))
    # print(rec_sys.item)
    # lst = [[1],[2], [3], [4]]
    rec_sys = RecommendationSystem()
    rec_sys.initialize()
    print(all(book_id not in GENRE_REPO for book_id in LIBRARY))  # TODO: here...
    print(len(rec_sys.subsystems))
    # print(len(rec_sys))




