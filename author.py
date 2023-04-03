"""CSC111 Winter 2023 Course Project: Book Recommendation System

Descriptions and Instructions
===============================
This module contains the function that is used to extract the author
information from the given dataset of authors and builds a dictionary
mapping the ID of each author to their name.

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

import gzip
import json


DATA_FILENAME = 'data/authors.json.gz'


def load_author_data() -> dict[int, str]:
    """
    Read and extract author json.gz data and return a mapping from author id to author name
    """

    data = []
    with gzip.open(DATA_FILENAME) as fin:
        for i in fin:
            d = json.loads(i)
            data.append(d)

    data = {int(author['author_id']): author['name'] for author in data}

    return data


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['gzip', 'json']
    })
