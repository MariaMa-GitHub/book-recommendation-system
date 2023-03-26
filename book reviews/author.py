"""
Book Author
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
    # print(load_genre_data())
    pass
