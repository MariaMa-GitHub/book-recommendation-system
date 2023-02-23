"""..."""
from __future__ import annotations
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta
import datetime
import json


BOOK_PATH = '/Users/kaiwenzheng/Desktop/goodreads_books_young_adult.json'
REVIEW_PATH = '/Users/kaiwenzheng/Desktop/goodreads_reviews_young_adult.json'
GENRE_PATH = '/Users/kaiwenzheng/Desktop/goodreads_book_genres_initial.json'
AUTHOR_PATH = '/Users/kaiwenzheng/Desktop/goodreads_book_authors.json'


@dataclass
class User:
    """..."""
    user_id: str
    birthday: datetime.datetime
    review_ids: dict[str, Review]
    genres_chosen: set[str]
    page_range: tuple[int, int]
    ebook_ok: bool
    bookshelf: dict[str, Book]

    def get_user_age(self) -> int:
        """Return the age of this user."""
        now = datetime.datetime.now()
        return relativedelta(now, self.birthday).years


@dataclass
class Book:
    """..."""
    book_id: str
    genres: dict[str, int]  # tags are extracted from users' popular shelves by a simple keyword matching process
    country_code: str
    language_code: str
    is_ebook: bool
    average_rating: float
    reviews: list[Review]
    similar_books: list[Book]
    description: str
    format: str
    link: str
    authors: list[Author]
    publisher: str
    publication_year: int
    num_pages: int
    url: str
    image_url: str
    title: str
    title_without_series: str

    def __lt__(self, other: Book) -> bool:
        return self.average_rating < other.average_rating


@dataclass
class Author:
    """..."""
    author_id: str
    author_name: str


@dataclass
class Review:
    """..."""
    user_id: str  # the user who wrote this review
    book_id: str
    review_id: str
    review_text: str
    rating: float


def get_authors(author_file: str) -> dict[str, Author]:
    """author_id --> Author object"""
    authors = {}
    for line in open(author_file):
        data = json.loads(line)
        authors[data['author_id']] = \
            Author(author_id=data['author_id'], author_name=data['name'])

    return authors


def book_genre_map(genre_file: str) -> dict[str, dict]:
    """book_id --> genre tags"""
    bgm = {}

    for line in open(genre_file):
        data = json.loads(line)
        bgm[data['book_id']] = data['genres']

    return bgm


def genre_book_map(genre_file: str) -> dict[str, set[str]]:
    """genre --> book_ids"""
    gbm = {}
    for line in open(genre_file):
        data = json.loads(line)
        genre_tags = data['genres']
        for genre in genre_tags:
            if genre not in gbm:
                gbm[genre] = {data['book_id']}
            else:
                gbm[genre].add(data['book_id'])
    return gbm


def book_review_map(review_file: str) -> dict[str, list[Review]]:
    """book_id --> Review objects"""
    reviews = {}

    for line in open(review_file):
        data = json.loads(line)
        review = Review(user_id=data['user_id'],
                        book_id=data['book_id'],
                        review_id=data['review_id'],
                        review_text=data['review_text'],
                        rating=data['rating'])
        if review.book_id not in reviews:
            reviews[review.book_id] = [review]
        else:
            reviews[review.book_id].append(review)

    return reviews


def get_book_repo(book_file: str, genre_file: str, review_file: str, author_file: str) -> dict[str, Book]:
    """book_id --> Book object"""
    bgm = book_genre_map(genre_file)
    brm = book_review_map(review_file)
    all_authors = get_authors(author_file)
    books = {}
    for line in open(book_file):
        data = json.loads(line)

        # is_ebook preprocessing
        if data['is_ebook'] == 'true':
            is_ebook = True
        else:
            is_ebook = False

        # authod_ids preprocessing
        author_ids = {author_list['author_id'] for author_list in data['authors']}
        authors = [all_authors[author_id] for author_id in author_ids]

        # num_pages preprocessing
        num_pages = 0
        if data['num_pages'] != '':
            num_pages = int(data['num_pages'])

        # review preprocessing:
        reviews = Review('', '', '', '', 0.0)
        try:
            reviews = brm[data['book_id']]
        except KeyError:
            pass

        book = Book(book_id=data['book_id'],
                    genres=bgm[data['book_id']],
                    country_code=data['country_code'],
                    language_code=data['language_code'],
                    is_ebook=is_ebook,
                    average_rating=float(data['average_rating']),
                    reviews=reviews,
                    similar_books=data['similar_books'],
                    description=data['description'],
                    format=data['format'],
                    link=data['link'],
                    authors=authors,
                    publisher=data['publisher'],
                    publication_year=data['publication_year'],
                    num_pages=num_pages,
                    url=data['url'],
                    image_url=data['image_url'],
                    title=data['title'],
                    title_without_series=data['title_without_series'])
        books[book.book_id] = book

    return books


book_repo = get_book_repo(BOOK_PATH, GENRE_PATH, REVIEW_PATH, AUTHOR_PATH)
gbm = genre_book_map(GENRE_PATH)
