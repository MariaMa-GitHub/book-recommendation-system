"""Manager System"""
from dateutil.relativedelta import relativedelta
from library import Book, User, Author, Review
import datetime
import recommendation_system_kwz
import relevance_system_kwz
# TODO: manager system to be completed...
# maps used ids to user objects


class ManagerSystem:
    """..."""
    users: dict[str, User]  # user_id --> User object

    def __init__(self) -> None:
        """..."""
        self.users = {}

    def add_user(self, user: User) -> None:
        """
        Preconditions:
            - user.user_id not in self.users
        """
        self.users[user.user_id] = user

    def add_book_for_user(self, user_id: str, book: Book) -> None:
        """
        Preconditions:
            - user_id in self.users
        """
        user = self.users[user_id]
        book_id = book.book_id
        if book_id not in user.bookshelf:
            user.bookshelf[book_id] = book
        else:
            ...
            # user-interface: display to user that this book cannot be added
            # because it's already presented in user's account
