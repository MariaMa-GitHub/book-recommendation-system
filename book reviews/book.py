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
    authors: dict[int, str]
    publisher: str
    publication_year: int
    country: str
    language: str
    num_pages: int
    popular_shelves: list[str]
    average_rating: float
    ratings_count: int
    description: str
    similar_books: set[int]
    link: str
    image: str

    def __init__(self, df: pandas.DataFrame, i: int):

        self.id = int(df.iloc[i]['book_id'])
        self.title = df.iloc[i]['title']
        self.authors = {int(author['author_id']): '' for author in df.iloc[i]['authors']}
        self.publisher = df.iloc[i]['publisher']
        self.publication_year = int(df.iloc[i]['publication_year'])
        self.country = df.iloc[i]['country_code']
        self.language = df.iloc[i]['language_code']
        self.num_pages = int(df.iloc[i]['num_pages'])
        self.genres = []
        self.average_rating = float(df.iloc[i]['average_rating'])
        self.ratings_count = int(df.iloc[i]['ratings_count'])
        self.description = df.iloc[i]['description']
        self.similar_books = {int(book_id) for book_id in df.iloc[i]['similar_books']}
        self.link = df.iloc[i]['link']
        self.image = df.iloc[i]['image_url']
