"""
Main Program
"""

import gzip
import json
import pandas
from numpy import nan

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

    # print(df.columns)
    # print(df.head())


def polish_data(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    Remove unwanted data from dataframe
    """

    columns_to_remove = ['isbn', 'text_reviews_count', 'series', 'asin', 'is_ebook', 'kindle_asin', 'format',
                         'isbn13', 'publication_day', 'publication_month', 'edition_information', 'url',
                         'work_id']

    df = df.drop(columns_to_remove, axis=1)

    df.replace('', nan, inplace=True)

    df.dropna(inplace=True)

    # df.drop_duplicates(subset=['book_id'])

    return df


def read_data() -> pandas.DataFrame:
    """
    Read dataframe data
    """
    return pandas.read_pickle(DATAFRAME_FILENAME)


def save_data(df: pandas.DataFrame) -> None:
    """
    Save dataframe data
    """

    df.to_pickle(DATAFRAME_FILENAME)


if __name__ == '__main__':

    try:
        df = read_data()
    except FileNotFoundError:
        save_data(load_data())
        df = read_data()

    # df = load_data()

    library = Library()
    library.load_books(df)

    print(len(library.books))
    print(df.columns)
    print(df.isna())
