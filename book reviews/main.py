"""
Main Program
"""

import gzip
import json
import pandas
from numpy import nan
from gui import Platform
from library import Library
DATA_FILENAME = '/Users/kaiwenzheng/Desktop/CURRENT/csc111-group-project-gui-maria/book reviews/data/books.json.gz'
DATAFRAME_FILENAME = '/Users/kaiwenzheng/Desktop/CURRENT/csc111-group-project-gui-maria/book reviews/data/dataframe.pkl'


def load_data() -> pandas.DataFrame:
    """
    Read book csv data and store it into a Pandas dataframe
    """

    data = []
    with gzip.open(DATA_FILENAME) as file:
        for i in file:
            d = json.loads(i)
            data.append(d)

    dataframe = pandas.DataFrame(data)
    dataframe = polish_data(dataframe)

    return dataframe


def polish_data(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    """
    Remove unwanted data (useless information, null values, etc.) from the given dataframe and return the new dataframe
    """

    columns_to_remove = ['isbn', 'text_reviews_count', 'series', 'asin', 'kindle_asin', 'format',
                         'isbn13', 'publication_day', 'publication_month', 'edition_information', 'url',
                         'work_id', 'image_url']

    dataframe = dataframe.drop(columns_to_remove, axis=1)

    dataframe.replace('', nan, inplace=True)

    dataframe.dropna(inplace=True)

    return dataframe


def read_data() -> pandas.DataFrame:
    """
    Read dataframe data from the saved pkl file
    """

    return pandas.read_pickle(DATAFRAME_FILENAME)


def save_data(dataframe: pandas.DataFrame) -> None:
    """
    Save dataframe data into a pkl file
    """

    dataframe.to_pickle(DATAFRAME_FILENAME)


try:
    df = read_data()
except FileNotFoundError:
    save_data(load_data())
    df = read_data()

library = Library()
library.load_books(df)

# counter = {}
# for book in library.books:
#     similar_books = library.books[book].similar_books
#     for sb in similar_books:
#         if sb not in counter:
#             counter[sb] = 1
#         else:
#             counter[sb] += 1
#
# print({book for book in counter if counter[book] >= 50 and book in library.books})

# print(all(isinstance(library.books[book].num_pages, int) for book in library.books))
# print(len(library.books))

# p = Platform(library.books)  TODO: to be uncommented...
# p.run()
