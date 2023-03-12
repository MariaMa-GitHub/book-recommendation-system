from __future__ import annotations
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta
from typing import Optional
import json
import pandas
import python_ta  # TODO: use it for contract checking


# TODO: please change the following directories to ones that appear on your machine
BOOK_PATH = '/Users/kaiwenzheng/Desktop/goodreads_books_young_adult.json'
REVIEW_PATH = '/Users/kaiwenzheng/Desktop/goodreads_reviews_young_adult.json'
GENRE_PATH = '/Users/kaiwenzheng/Desktop/goodreads_book_genres_initial.json'
AUTHOR_PATH = '/Users/kaiwenzheng/Desktop/goodreads_book_authors.json'


@dataclass
class Book:
    """A book class."""
    # Private Instance Attributes:
    #   - _country_code: the country code of this book
    #   - _language code: the language code of this book
    #   - _is ebook: whether this book is an E-book
    #   - _average rating: the average rating of this book
    #   - _similar books: a list of IDs of books that users who like the current book also like
    #   - _description: the description of this book
    #   - _link: the link of this book on Goodreads
    #   - _authors: the authors of this book
    #   - _num pages: the number of pages this book has
    #   - _publication year: the year in which this book was published
    #   - _book id: the ID of this book
    #   - _ratings count: the number of ratings given to this book
    #   - _title: the title of this book
    _country_code: str
    _language_code: str
    _is_ebook: bool  # TODO: convert str to bool
    _average_rating: Optional[float]  # TODO: convert str to float
    _similar_books: list[str]  # a list of book ids
    _description: str  # description text
    _link: str  # url link of this book
    _authors: list[str]  # a list of author ids
    _publisher: str  # name of the publisher
    _num_pages: Optional[int]  # TODO: convert str to int
    _publication_year: Optional[int]  # TODO: convert str to int
    _book_id: str  # the id of this book
    _rating_count: Optional[int]  # TODO: convert str to int
    _title: str

    # @property
    # def country_code(self) -> str:
    #     """TODO: ..."""
    #     return self._country_code
    
    # @property
    # def language_code(self) -> str:
    #     """TODO: ..."""
    #     return self._language_code
    
    # @property
    # def is_ebook(self) -> bool:
    #     """TODO: ..."""
    #     return self._is_ebook
    
    # @property
    # def average_rating(self) -> Optional[float]:
    #     """TODO: ..."""
    #     return self._average_rating
    
    # @property
    # def similar_books(self) -> list[str]:
    #     """TODO: ..."""
    #     return self._similar_books
    
    # @property
    # def description(self) -> str:
    #     """TODO: ..."""
    #     return self._description
    
    # @property
    # def link(self) -> str:
    #     """TODO: ..."""
    #     return self._link
    
    # @property
    # def authors(self) -> list[str]:
    #     """TODO: ..."""
    #     return self._authors
    
    # @property
    # def publisher(self) -> str:
    #     """TODO: ..."""
    #     return self._publisher
    
    # @property
    # def num_pages(self) -> Optional[int]:
    #     """TODO: ..."""
    #     return self._num_pages
    
    # @property
    # def publication_year(self) -> Optional[int]:
    #     """TODO: ..."""
    #     return self._publication_year
    
    # @property
    # def book_id(self) -> str:
    #     """TODO: ..."""
    #     return self._book_id
    
    # @property
    # def rating_count(self) -> Optional[int]:
    #     """TODO: ..."""
    #     return self._rating_count
    
    # @property
    # def title(self) -> str:
    #     """TODO: ..."""
    #     return self._title

    # def __lt__(self, other: Book) -> bool:
    #     return self.average_rating < other.average_rating


@dataclass
class Author:
    """An author class."""
    # Private Instance Attributes:
    #   - _author_id: the ID of this authors
    #   - _name: the name of this author
    _author_id: str
    _name: str


@dataclass
class Review:
    """A review class. This represents a review of a book given by
    a user.
    """
    # Private Instance Attributes:
    #   - _user id: the ID of the user reviewing this book
    #   - _book id: the ID of this book
    #   - _review id: the ID of the review provided by this user
    #   - _rating: the rating given by this user
    #   - _review text: the review text written by this user
    #   - _date added: the date the review was added
    #   - _date updated: the date the review was updated
    _user_id: str
    _book_id: str
    _review_id: str
    _rating: Optional[float]
    _review_text: str
    _date_added: str
    _date_updated: str


def build_genre_repo(genre_file: str) -> dict[str, list[str]]:
    """Use the information in genre_file to directly modify genre_repo
    to construct a mapping from each genre to a list of IDs of books
    with the corresponding genre.
    
    Preconditions:
        - genre_repo == {}
        - genre_repo is a valid JSON file
    """
    genre_repo = {}
    for line in open(genre_file):
        data = json.loads(line)
        for genre in data['genres']:
            if genre not in genre_repo:
                genre_repo[genre] = [data['book_id']]
            else:
                genre_repo[genre].append(data['book_id'])
    return genre_repo

def build_book_repo(book_file: str) -> dict[str, Book]:
    """Use the information in book_file to directly modify book_repo
    to construct a mapping from the ID of each book to the Book object
    corresponding to that ID.
    
    Preconditions:
        - book_repo == {}
        - book_file is a valid JSON file
    """
    book_repo = {}
    for line in open(book_file):
        data = json.loads(line)
        country_code = data['country_code']
        language_code = data['language_code']
        is_ebook = data['is_ebook']
        average_rating = data['average_rating']
        similar_books = data['similar_books']
        description = data['description']
        link = data['link']
        authors = data['authors']
        publisher = data['publisher']
        num_pages = data['num_pages']
        publication_year = data['publication_year']
        book_id = data['book_id']
        rating_count = data['ratings_count']
        title = data['title']
        
        if is_ebook == 'true':
            is_ebook = True
        else:
            is_ebook = False

        if average_rating == '':
            average_rating = None
        else:
            average_rating = float(average_rating)

        if num_pages == '':
            num_pages = None
        else:
            num_pages = int(num_pages)

        if publication_year == '':
            publication_year = None
        else:
            publication_year = int(publication_year)

        if rating_count == '':
            rating_count = None
        else:
            rating_count = int(rating_count)

        book = Book(country_code, language_code, is_ebook, average_rating, 
                    similar_books, description, link, authors, publisher,
                    num_pages, publication_year, book_id, rating_count, title)
        book_repo[book_id] = book

    return book_repo    


def build_review_repo(review_file: str) -> dict[str, dict[str, Review]]:
    """Use the information in review_file to directly modify review_repo
    to construct a mapping from the ID of each book to a dictionary of
    reviews for this book, where each dictionary stores a mapping from
    the ID of each review to the corresponding review object.
    
    Preconditions:
        - review_repo == {}
        - review_file is a valid JSON file
    """
    review_repo = {}
    for line in open(review_file):
        data = json.loads(line)
        user_id = data['user_id']
        book_id = data['book_id']
        review_id = data['review_id']
        rating = data['rating']
        review_text = data['review_text']
        date_added = data['date_added']
        date_updated = data['date_updated']

        if rating == '':
            rating = None
        else:
            rating = float(rating)

        review = Review(user_id, book_id, review_id, rating,
                        review_text, date_added, date_updated)
        if book_id not in review_repo:
            review_repo[book_id] = {review_id: review}
        else:
            review_repo[book_id][review_id] = review


# book_repo, genre_repo, review_repo = {}, {}, {}
book_repo = build_book_repo(BOOK_PATH)
genre_repo = build_genre_repo(GENRE_PATH)
review_repo = build_review_repo(REVIEW_PATH)
print(any(book_id in genre_repo for book_id in book_repo))  # TODO: here...
print(f'len(book_repo): {len(book_repo)}')


