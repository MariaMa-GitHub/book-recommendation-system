"""
Main Program
"""

import gzip
import json
import pandas
from numpy import nan
from gui import Platform
from library import Library

DATA_FILENAME = 'data/books.json.gz'
DATAFRAME_FILENAME = 'data/dataframe.pkl'


def load_data() -> pandas.DataFrame:
    """
    Read csv data and store it into a dataframe
    """

    count = 0
    data = []
    with gzip.open(DATA_FILENAME) as fin:
        for i in fin:
            d = json.loads(i)
            count += 1
            data.append(d)

    df = pandas.DataFrame(data)
    df = polish_data(df)

    return df


def polish_data(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    """
    Remove unwanted data from dataframe
    """

    columns_to_remove = ['isbn', 'text_reviews_count', 'series', 'asin', 'kindle_asin', 'format',
                         'isbn13', 'publication_day', 'publication_month', 'edition_information', 'url',
                         'work_id']

    dataframe = dataframe.drop(columns_to_remove, axis=1)

    dataframe.replace('', nan, inplace=True)

    dataframe.dropna(inplace=True)

    return dataframe


def read_data() -> pandas.DataFrame:
    """
    Read dataframe data
    """

    return pandas.read_pickle(DATAFRAME_FILENAME)


def save_data(dataframe: pandas.DataFrame) -> None:
    """
    Save dataframe data
    """

    dataframe.to_pickle(DATAFRAME_FILENAME)


if __name__ == '__main__':

    try:
        df = read_data()
    except FileNotFoundError:
        save_data(load_data())
        df = read_data()

    # df = load_data()

    library = Library()
    library.load_books(df)

    p = Platform(library.books)
    p.run()
