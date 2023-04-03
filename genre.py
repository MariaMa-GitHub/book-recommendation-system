"""CSC111 Winter 2023 Course Project: Book Recommendation System

Descriptions and Instructions
===============================
This module contains the genre filter used to assign genre tags to
each book in the library constructed in library.py. The resulting
genre tags are used for the purpose of displaying as part of the
book description in the graphical user interface (GUI).

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


def filter_genres(genres: set[str]) -> set[str]:
    """Filter given book genres by removing unwanted genres (making them much
    more specific than shelf names).
    """

    genres_to_keep = {
        'romance', 'fiction', 'young adult', 'high school', 'realistic fiction', 'mythology',
        'suspense', 'survival', 'time travel', 'action', 'coming of age', 'post apocalyptic',
        'humor', 'supernatural', 'fantasy', 'science fiction', 'nonfiction', 'teen', 'childrens',
        'historical fiction', 'mystery', 'short stories', 'horror', 'magic', 'gay', 'lesbian',
        'paranormal', 'middle grade', 'contemporary', 'dystopia', 'thriller', 'lgbt', 'queer',
        'adventure', 'classics'
    }

    return {genre for genre in genres if genre in genres_to_keep}


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
