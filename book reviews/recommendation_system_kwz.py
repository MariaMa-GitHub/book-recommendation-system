"""
If the given user has no past reading records stores in the manager system OR the user
with an existing account wants to explore books whose genres are not contained in this
user's past reading activities, use this decision-tree-based recommendation system (called
a recommendation system) to make recommendations.
"""
from __future__ import annotations
from typing import Any
import library

SYSTEM_START = '*'
LIBRARY = library.book_repo
# ORDERED_LIBRARY = library.book_list
GENRE_BOOK_MAP = library.gbm


class RecommendationSystem:
    """A recommendation system based on the decision tree. This system is used when
    either the user has no account recorded or the user wants to explore books of genres
    which haven't appeared in this user's past reading activities.
    """
    item: Any
    subsystems: list[RecommendationSystem]

    def __init__(self, root: Any = SYSTEM_START) -> None:
        """Initialize this recommendation system."""
        self.item = root
        self.subsystems = []

    def add_subsystem(self, subsystem: RecommendationSystem) -> None:
        """Add a subsystem to this recommendation system."""
        self.subsystems.append(subsystem)

    def recommend(self, responses: list) -> list[str]:
        """Return a list of IDs of recommended books based on the user's responses to a
        sequence of pre-set questions.

        This sequence of questions includes the following:
            1. Is the user's age at least 18 years old?
            2. What genres would the user like to select?
            3. What range of number of pages of a book does the user prefer?
            4. Does the user accept E-book?

        Preconditions:
            - isinstance(responses[0], bool)
            - isinstance(responses[1], set)
            - isinstance(responses[2], tuple)
            - isinstance(responses[3], bool)
        """
        adult, genres, num_pages_range, ebook_ok = responses[0], responses[1], responses[2], responses[3]
        if adult:
            curr_system = self.subsystems[1]
        else:
            curr_system = self.subsystems[0]

        subsystem_indicies = self.find_subsystems_by_genres(genres)
        all_recommendations = []
        for index in subsystem_indicies:
            if index != -1:
                recommendations = curr_system.subsystems[index].explore(num_pages_range, ebook_ok)
                all_recommendations.extend(recommendations)

        return all_recommendations

    def find_subsystems_by_genres(self, genres: set[str]) -> list[int]:
        """Return a list of indicies indicating the position of the subsystem containing the given genre
        in genres.

        Preconditions:
            - isinstance(self.item, bool)
        """
        indicies = []
        for genre in genres:
            i = 0
            while i < len(self.subsystems) and self.subsystems[i].item != genre:
                i += 1

            if i == len(self.subsystems):
                indicies.append(-1)
            else:
                indicies.append(i)

        return indicies

    def explore(self, num_pages_range: tuple[int, int], ebook_ok: bool) -> list[str]:
        """Return a list of IDs of the recommended books based on the user's responses
        on the range of the number of pages the user prefers and whether the user accpets
        the E-book.

        Preconditions:
            - isinstance(self.item, dict)
            - self.subsystems == []
        """
        recommendation_result = []
        genre = list(self.item.keys())[0]
        book_ids = self.item[genre]
        for book_id in book_ids:
            book = LIBRARY[book_id]
            if book.num_pages in range(num_pages_range[0], num_pages_range[1] + 1) or \
                    book.is_ebook == ebook_ok:  # TODO: second condition to be modified...
                recommendation_result.append((book.average_rating, book_id))

        recommendation_result.sort(reverse=True)
        for i in range(len(recommendation_result)):
            recommendation_result[i] = recommendation_result[i][1]

        return recommendation_result


def initialize_system() -> RecommendationSystem:
    """Initialize a decision-tree-based recommendation system."""
    system = RecommendationSystem()
    underage_system = RecommendationSystem(False)
    adult_system = RecommendationSystem(True)
    # TODO: separate underage books with others with additional information
    for genre in GENRE_BOOK_MAP:
        underage_system.add_subsystem(RecommendationSystem(genre))
    for genre in GENRE_BOOK_MAP:
        adult_system.add_subsystem(RecommendationSystem(genre))

    system.add_subsystem(underage_system)
    system.add_subsystem(adult_system)

    return system


if __name__ == '__main__':
    pass
