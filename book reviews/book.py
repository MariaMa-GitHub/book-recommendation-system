"""
Book Class
"""
import pandas


class Book:
    """
    Contain all the information of a book
    """

    id: int
    title: str
    authors: list[str]
    publisher: str
    publication_year: int
    country: str
    language: str
    num_pages: int
    popular_shelves: list[str]
    average_rating: float
    ratings_count: int
    description: str
    similar_books: list[int]
    link: str
    image: str

    def __init__(self, df: pandas.DataFrame, i: int):

        self.id = df.iloc[i]['book_id']
        self.title = df.iloc[i]['title']
        self.authors = [str(df.iloc[i]['authors'])]
        self.publisher = df.iloc[i]['publisher']
        self.publication_year = df.iloc[i]['publication_year']
        self.country = df.iloc[i]['country_code']
        self.language = df.iloc[i]['language_code']
        self.num_pages = df.iloc[i]['num_pages']
        self.popular_shelves = [str(df.iloc[i]['popular_shelves'])]
        self.average_rating = df.iloc[i]['average_rating']
        self.ratings_count = df.iloc[i]['ratings_count']
        self.description = df.iloc[i]['description']
        self.similar_books = df.iloc[i]['similar_books']
        self.link = df.iloc[i]['link']
        self.image = df.iloc[i]['image_url']

    def __str__(self):

        return f'{self.id}, {self.title}: link {self.link}, rating = {self.average_rating}'
