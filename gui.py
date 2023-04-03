"""CSC111 Winter 2023 Course Project: Book Recommendation System

Descriptions and Instructions
===============================
This module contains the design of the interactive graphical user
interface (GUI) our recommendation use.

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

from typing import Any
import sys

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from book import Book
from recommendation_system import RecommendationSystem, SimilarBookSystem

APP_TITLE = 'Book Recommendation System'
W_HEIGHT = 600
W_WIDTH = 800


class Platform:
    """Program GUI (Graphical User Interface).

    Instance Attributes:
        - app: GUI application
        - window: main window of the GUI application
    """
    app: QApplication
    window: QMainWindow

    def __init__(self, books: dict[int, Book]) -> None:
        """Initialize the platform with the GUI.

        Representation Invariants:
            - books != {}
        """
        self.app = QApplication([])
        self.window = Window(books)

    def run(self) -> None:
        """Run the GUI."""
        self.window.setFocus()
        self.window.show()
        self.app.exec()


class Window(QMainWindow):
    """Main window of the program GUI.

    Instance Attributes:
        - data: book preferences that user enter
        - categories: what the user can choose from for each category of book preferences
        - current_book: the ID of the book the user is currently viewing
        - books: the repository of all books
        - saved_books: ids of books saved by the user
        - similar_books: similar books based on the user's book preferences and saved books
        - current_window: the window the user is currently viewing (for the book preferences section)
        - num_windows: the total number of windows (for the book preferences section)
        - rec_sys: book recommendation system
        - sim_sys: similar book recommendation system
        - book_id_src: text box for user to enter desired book id
        - book_lst: list that displays recommended books, saved books, and similar books
        - book_txt: giant text box that displays the chosen book's detailed information
        - window_layout: program window layout
        - min_pages_sld: slider for user to choose desired minimum of pages
        - min_pages_lbl: label that displays the user's desired minimum of pages
        - max_pages_sld: slider for user to choose desired maximum of pages
        - max_pages_lbl: label that displays the user's desired maximum of pages
        - country_lst: list for user to choose desired book countries
        - language_lst: list for user to choose desired book languages
        - title_src: text box for user to enter desired book title
        - author_src: text box for user to enter desired book author
        - publisher_src: text box for user to enter desired book publisher
        - pub_year_src: text box for user to enter desired book publication year
        - ebook_rad: radio button to choose whether the user wants books that are available in ebook format
        - btn_exit: program exit button
    """
    data: dict[str, Any]
    categories: dict[str, list[Any]]
    current_book: int
    books: dict[int, Book]
    recommended_books: dict[int, Book]
    saved_books: set[int]
    similar_books: set[int]
    current_window: int
    num_windows: int
    rec_sys: RecommendationSystem
    sim_sys: SimilarBookSystem
    book_id_src: QLineEdit
    book_lst: QListWidget
    book_txt: QTextEdit
    window_layout: QStackedLayout
    min_pages_sld: QSlider
    min_pages_lbl: QLabel
    max_pages_sld: QSlider
    max_pages_lbl: QLabel
    country_lst: QListWidget
    language_lst: QListWidget
    title_src: QLineEdit
    author_src: QLineEdit
    publisher_src: QLineEdit
    pub_year_src: QLineEdit
    ebook_rad: QRadioButton
    btn_exit: QPushButton

    def __init__(self, books: dict[int, Book]) -> None:
        """Initialize the main window of the GUI.

        Representation Invariants:
            - books != {}
        """
        super().__init__(None)

        self.data = {}
        self.categories = {
            'country': list({books[book].country for book in books}),
            'language': sorted(list({books[book].language for book in books})),
            'title': list({books[book].title for book in books}),
            'author': list({f'{books[book].authors[author]} (ID {author})'
                            for book in books for author in books[book].authors}),
            'publisher': list({books[book].publisher for book in books}),
            'publication year': list({str(books[book].publication_year) for book in books})
        }
        self.current_book = 0
        self.books = books
        self.recommended_books = {}
        self.similar_books = set()
        self.saved_books = set()

        self.rec_sys = RecommendationSystem(books)
        self.rec_sys.initialize()
        self.sim_sys = SimilarBookSystem(books)
        self.sim_sys.initialize()

        self.current_window = 0
        self.num_windows = 0
        self.setWindowTitle(APP_TITLE)
        self.setFixedSize(QSize(W_WIDTH, W_HEIGHT))

        dialog = QMessageBox()
        dialog.setText('Do you want to get book recommendations?')
        dialog.setIcon(QMessageBox.Icon.Question)
        dialog.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
        dialog.setDefaultButton(QMessageBox.StandardButton.Yes)
        dialog.setWindowTitle('Welcome!')
        result = dialog.exec()

        if result == QMessageBox.StandardButton.Yes:
            self.recommendation_search()
        else:
            self.similar_books_search()

    def similar_books_search(self) -> None:
        """Allow the user to searchfor similar books based on their library."""
        widget = QWidget(self)
        page_layout = QGridLayout(widget)
        page_layout.setContentsMargins(70, 70, 70, 70)

        self.book_id_src = QLineEdit()
        self.book_id_src.setPlaceholderText('Enter Book ID')
        self.book_id_src.setFont(QFont('Arial', 20))
        self.book_id_src.setTextMargins(5, 5, 5, 5)
        book_id_cpl = QCompleter([str(book) for book in self.books.keys()], self.book_id_src)
        book_id_cpl.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.book_id_src.setCompleter(book_id_cpl)

        self.book_lst = QListWidget(None)
        self.book_lst.setFont(QFont('Arial', 16))
        self.update_book_status()
        self.book_lst.addItems(self.get_recommended_books())
        self.book_lst.addItems(self.get_saved_books())
        self.book_lst.addItems(self.get_similar_books())
        self.book_lst.itemPressed.connect(self.select_book_id)

        # book info
        self.book_txt = QTextEdit()
        self.book_txt.setText('Book Recommendation System Instructions\n\n\n'
                              '* To see detailed book description, please first click on '
                              'the book you are interested in and then press "Search".\n\n\n'
                              '* To save a book, click on the book you want to save, click '
                              'on "Search" and then press "Save". You will see a message '
                              'indicating that you have successfully saved the book.\n\n\n'
                              '* To un-save a book, click on the book you want to remove from '
                              'the system, click on "Search", and then press "Unsave". You '
                              'will see a message indicating that you have successfully saved '
                              'the book.\n')
        self.book_txt.setFont(QFont('Arial', 16))
        self.book_txt.setReadOnly(True)

        # random space
        space = QLabel('')
        space.setFixedWidth(5)

        # save button
        btn_save = QPushButton('Save')
        btn_save.setFont(QFont('Arial', 18))
        btn_save.setFixedSize(150, 50)
        btn_save.pressed.connect(self.save_book_id)

        # unsave button
        btn_unsave = QPushButton('Unsave')
        btn_unsave.setFont(QFont('Arial', 18))
        btn_unsave.setFixedSize(150, 50)
        btn_unsave.pressed.connect(self.unsave_book_id)

        page_layout.addWidget(self.book_id_src, 0, 0, 1, 2)
        page_layout.addWidget(self.book_lst, 1, 0, 1, 2)
        page_layout.addWidget(self.book_txt, 0, 3, 2, 2)
        page_layout.addWidget(space, 3, 2)
        page_layout.addWidget(btn_save, 3, 3)
        page_layout.addWidget(btn_unsave, 3, 4)

        # restart button
        btn_restart = QPushButton('Restart')
        btn_restart.setFont(QFont('Arial', 18))
        btn_restart.setFixedSize(120, 50)
        btn_restart.pressed.connect(self.recommendation_search)
        page_layout.addWidget(btn_restart, 3, 0)

        # search button
        btn_search = QPushButton('Search')
        btn_search.setFont(QFont('Arial', 18))
        btn_search.setFixedSize(120, 50)
        btn_search.pressed.connect(self.search_book)
        page_layout.addWidget(btn_search, 3, 1)

        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def recommendation_search(self) -> None:
        """Allow the user to enter their preferences and receive book recommendations."""
        self.current_window = 0
        windows = []
        page_layout = QVBoxLayout()
        self.window_layout = QStackedLayout()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(250, 30, 250, 70)
        page_layout.addLayout(self.window_layout)
        page_layout.addLayout(button_layout)

        # first window
        widget1 = QWidget(None)
        layout1 = QGridLayout(widget1)
        program_lbl = QLabel('\nYoung Adult Book\nRecommendation System')
        program_lbl.setFont(QFont('Times New Roman', 48))
        program_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(program_lbl)
        widget1.setLayout(layout1)
        windows.append(widget1)

        # second window
        widget2 = QWidget(None)
        layout2 = QGridLayout(widget2)
        layout2.setContentsMargins(50, 50, 50, 20)
        min_pages_lbl0 = QLabel('Minimum Number of Pages\n')
        min_pages_lbl0.setFont(QFont('Times New Roman', 28))
        min_pages_lbl0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        min_pages_lbl1 = QLabel('0')
        min_pages_lbl1.setFont(QFont('Arial', 16))
        min_pages_lbl1.setFixedWidth(50)
        min_pages_lbl1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        min_pages_lbl2 = QLabel('500')
        min_pages_lbl2.setFont(QFont('Arial', 16))
        min_pages_lbl2.setFixedWidth(50)
        min_pages_lbl2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.min_pages_sld = QSlider(Qt.Orientation.Horizontal)
        self.min_pages_sld.setGeometry(50, 50, 200, 50)
        self.min_pages_sld.setMinimum(0)
        self.min_pages_sld.setMaximum(500)
        self.min_pages_sld.valueChanged.connect(self.value_changed_min_pages)
        self.min_pages_sld.setTickInterval(50)
        self.min_pages_lbl = QLabel('0 pages')
        self.min_pages_lbl.setFont(QFont('Arial', 18))
        self.min_pages_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        max_pages_lbl0 = QLabel('Maximum Number of Pages\n')
        max_pages_lbl0.setFont(QFont('Times New Roman', 28))
        max_pages_lbl0.setAlignment(Qt.AlignmentFlag.AlignCenter)
        max_pages_lbl1 = QLabel('0')
        max_pages_lbl1.setFont(QFont('Arial', 16))
        max_pages_lbl1.setFixedWidth(50)
        max_pages_lbl1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        max_pages_lbl2 = QLabel('1000')
        max_pages_lbl2.setFont(QFont('Arial', 16))
        max_pages_lbl2.setFixedWidth(50)
        max_pages_lbl2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.max_pages_sld = QSlider(Qt.Orientation.Horizontal)
        self.max_pages_sld.setGeometry(50, 50, 200, 50)
        self.max_pages_sld.setMinimum(0)
        self.max_pages_sld.setMaximum(1000)
        self.max_pages_sld.valueChanged.connect(self.value_changed_max_pages)
        self.max_pages_sld.setTickInterval(50)
        self.max_pages_lbl = QLabel('0 pages')
        self.max_pages_lbl.setFont(QFont('Arial', 18))
        self.max_pages_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout2.addWidget(min_pages_lbl0, 0, 1)
        layout2.addWidget(min_pages_lbl1, 1, 0)
        layout2.addWidget(self.min_pages_sld, 1, 1)
        layout2.addWidget(min_pages_lbl2, 1, 2)
        layout2.addWidget(self.min_pages_lbl, 2, 1)
        layout2.addWidget(QLabel(''), 3, 1)
        layout2.addWidget(max_pages_lbl0, 4, 1)
        layout2.addWidget(max_pages_lbl1, 5, 0)
        layout2.addWidget(self.max_pages_sld, 5, 1)
        layout2.addWidget(max_pages_lbl2, 5, 2)
        layout2.addWidget(self.max_pages_lbl, 6, 1)
        widget2.setLayout(layout2)
        windows.append(widget2)

        # third window
        widget3 = QWidget(None)
        layout3 = QGridLayout(widget3)
        layout3.setContentsMargins(50, 50, 50, 20)
        country_lbl = QLabel('Country')
        country_lbl.setStyleSheet('margin-bottom: 10px')
        country_lbl.setFont(QFont('Times New Roman', 28))
        country_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.country_lst = QListWidget(None)
        self.country_lst.setFont(QFont('Arial', 18))
        self.country_lst.addItems(self.categories['country'])
        self.country_lst.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.country_lst.setFixedSize(300, 100)
        language_lbl = QLabel('Language')
        language_lbl.setStyleSheet('margin-bottom: 10px')
        language_lbl.setFont(QFont('Times New Roman', 28))
        language_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.language_lst = QListWidget(None)
        self.language_lst.setFont(QFont('Arial', 18))
        self.language_lst.addItems(self.categories['language'])
        self.language_lst.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.language_lst.setFixedSize(300, 100)
        layout3.addWidget(country_lbl, 0, 1)
        layout3.addWidget(self.country_lst, 1, 1)
        layout3.addWidget(QLabel(''), 2, 1)
        layout3.addWidget(language_lbl, 3, 1)
        layout3.addWidget(self.language_lst, 4, 1)
        widget3.setLayout(layout3)
        windows.append(widget3)

        # fourth window
        widget4 = QWidget(None)
        layout4 = QGridLayout(widget4)
        layout4.setContentsMargins(50, 50, 50, 20)
        title_lbl = QLabel('Title')
        title_lbl.setFont(QFont('Times New Roman', 28))
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_src = QLineEdit()
        self.title_src.setPlaceholderText('Optional')
        self.title_src.setFont(QFont('Arial', 20))
        self.title_src.setFixedSize(250, 40)
        self.title_src.setTextMargins(5, 5, 5, 5)
        title_cpl = QCompleter(self.categories['title'], self.title_src)
        title_cpl.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.title_src.setCompleter(title_cpl)
        author_lbl = QLabel('Author')
        author_lbl.setFont(QFont('Times New Roman', 28))
        author_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.author_src = QLineEdit()
        self.author_src.setPlaceholderText('Optional')
        self.author_src.setFont(QFont('Arial', 20))
        self.author_src.setFixedSize(250, 40)
        self.author_src.setTextMargins(5, 5, 5, 5)
        author_cpl = QCompleter(self.categories['author'], self.author_src)
        author_cpl.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.author_src.setCompleter(author_cpl)
        publisher_lbl = QLabel('Publisher')
        publisher_lbl.setFont(QFont('Times New Roman', 28))
        publisher_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.publisher_src = QLineEdit()
        self.publisher_src.setPlaceholderText('Optional')
        self.publisher_src.setFont(QFont('Arial', 20))
        self.publisher_src.setFixedSize(250, 40)
        self.publisher_src.setTextMargins(5, 5, 5, 5)
        publisher_cpl = QCompleter(self.categories['publisher'], self.publisher_src)
        publisher_cpl.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.publisher_src.setCompleter(publisher_cpl)
        pub_year_lbl = QLabel('Publication Year')
        pub_year_lbl.setFont(QFont('Times New Roman', 28))
        pub_year_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pub_year_src = QLineEdit()
        self.pub_year_src.setPlaceholderText('Optional')
        self.pub_year_src.setFont(QFont('Arial', 20))
        self.pub_year_src.setFixedSize(250, 40)
        self.pub_year_src.setTextMargins(5, 5, 5, 5)
        pub_year_cpl = QCompleter(self.categories['publication year'], self.pub_year_src)
        pub_year_cpl.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.pub_year_src.setCompleter(pub_year_cpl)
        self.ebook_rad = QRadioButton('Ebook Available')
        self.ebook_rad.setFont(QFont('Arial', 20))
        self.ebook_rad.setStyleSheet('margin-top: 50px')
        layout4.addWidget(title_lbl, 0, 0)
        layout4.addWidget(self.title_src, 1, 0)
        layout4.addWidget(QLabel(''), 2, 0)
        layout4.addWidget(publisher_lbl, 3, 0)
        layout4.addWidget(self.publisher_src, 4, 0)
        layout4.addWidget(author_lbl, 0, 1)
        layout4.addWidget(self.author_src, 1, 1)
        layout4.addWidget(QLabel(''), 2, 1)
        layout4.addWidget(pub_year_lbl, 3, 1)
        layout4.addWidget(self.pub_year_src, 4, 1)
        layout4.addWidget(self.ebook_rad, 5, 0, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        widget4.setLayout(layout4)
        windows.append(widget4)

        # exit button
        self.btn_exit = QPushButton('Exit')
        self.btn_exit.setFont(QFont('Arial', 18))
        self.btn_exit.setFixedSize(120, 50)
        self.btn_exit.pressed.connect(self.activate_prev_window)
        button_layout.addWidget(self.btn_exit)

        # continue button
        btn_continue = QPushButton('Continue')
        btn_continue.setFont(QFont('Arial', 18))
        btn_continue.setFixedSize(120, 50)
        btn_continue.pressed.connect(self.activate_next_window)
        button_layout.addWidget(btn_continue)

        # all windows
        for window in windows:
            self.window_layout.addWidget(window)
            self.num_windows += 1

        widget = QWidget(self)
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def activate_next_window(self) -> None:
        """Switch to next window."""
        error = False

        if self.current_window == 0:
            self.btn_exit.setText('Back')
        elif self.current_window == 1:
            self.data['min_num_pages'] = self.min_pages_sld.value()
            self.data['max_num_pages'] = self.max_pages_sld.value()
            if self.data['min_num_pages'] > self.data['max_num_pages']:
                error = True
                dialog = QMessageBox()
                dialog.setText(
                    'The minimum number of pages is greater than the maximum number of pages.\n\nPlease try again.'
                )
                dialog.setIcon(QMessageBox.Icon.Warning)
                dialog.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
                dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
                dialog.setWindowTitle('Warning!')
                dialog.exec()
            elif self.data['max_num_pages'] - self.data['min_num_pages'] <= 5:
                error = True
                dialog = QMessageBox()
                dialog.setText(
                    'The range chosen is too restricted.\n\nPlease try again.'
                )
                dialog.setIcon(QMessageBox.Icon.Warning)
                dialog.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
                dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
                dialog.setWindowTitle('Warning!')
                dialog.exec()
        elif self.current_window == 2:
            self.data['country'] = [item.text() for item in self.country_lst.selectedItems()]
            self.data['language'] = [item.text() for item in self.language_lst.selectedItems()]

            if self.data['country'] == [] or self.data['language'] == []:
                error = True
                dialog = QMessageBox()
                dialog.setText(
                    'These fields are mandatory.\n\nPlease choose a value.'
                )
                dialog.setIcon(QMessageBox.Icon.Warning)
                dialog.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
                dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
                dialog.setWindowTitle('Warning!')
                dialog.exec()

        elif self.current_window == 3:
            if self.title_src.text() in self.categories['title'] and self.title_src.text() != '':
                self.data['title'] = self.title_src.text()
            else:
                self.data['title'] = None
            if self.author_src.text() in self.categories['author'] and self.author_src.text() != '':
                self.data['author'] = int(self.author_src.text().split(' (ID')[1][:-1])
            else:
                self.data['author'] = None
            if self.publisher_src.text() in self.categories['publisher'] and self.publisher_src.text() != '':
                self.data['publisher'] = self.publisher_src.text()
            else:
                self.data['publisher'] = None
            if self.pub_year_src.text() in self.categories['publication year'] and self.pub_year_src.text() != '':
                self.data['publication year'] = self.pub_year_src.text()
            else:
                self.data['publication year'] = None
            if self.ebook_rad.isChecked():
                self.data['is_ebook'] = True
            else:
                self.data['is_ebook'] = None

            self.recommend_books([(self.data['min_num_pages'], self.data['max_num_pages']),
                                  self.data['country'],
                                  self.data['language'],
                                  self.data['title'],
                                  self.data['author'],
                                  self.data['publisher'],
                                  self.data['publication year'],
                                  self.data['is_ebook']])
            self.similar_books_search()

        if not error:
            index = (self.current_window + 1) % self.num_windows
            self.window_layout.setCurrentIndex(index)
            self.current_window = index

    def activate_prev_window(self) -> None:
        """Switch to next window."""
        if self.current_window == 0:
            sys.exit()
        elif self.current_window == 1:
            self.btn_exit.setText('Exit')

        index = (self.current_window - 1) % self.num_windows
        self.window_layout.setCurrentIndex(index)
        self.current_window = index

    def value_changed_min_pages(self, i: int) -> None:
        """Display the chosen minimum number of pages."""
        self.min_pages_lbl.setText(f'{i} page(s)')

    def value_changed_max_pages(self, i: int) -> None:
        """Display the chosen maximum number of pages."""
        self.max_pages_lbl.setText(f'{i} page(s)')

    def select_book_id(self, book: Any) -> None:
        """Fill the book ID searchbar with the ID of the selected book."""
        book_info = book.text()
        index = book_info.find(':')
        self.book_id_src.setText(book_info[3:index])

    def search_book(self) -> None:
        """Display information of chosen book."""
        if self.book_id_src.text().strip() in {str(book_id) for book_id in self.books}:
            self.current_book = int(self.book_id_src.text())
            self.book_txt.setText(self.get_book_info())

    def recommend_books(self, preferences: list[Any]) -> None:
        """Recommend books with a recommendation system based on user preferences.

        Preconditions:
            - len(preferences) == 8
        """
        book_ids = self.rec_sys.recommend(preferences)
        self.recommended_books = {book_id: self.books[book_id] for book_id in book_ids}

    def get_recommended_books(self) -> list[str]:
        """Return a list of id + title for the list of recommended books."""
        recommended_books = []
        sorted_recommended_books = sorted(list(self.recommended_books.values()),
                                          key=lambda x: (x.average_rating, x.ratings_count))[::-1]

        for book in sorted_recommended_books:
            if book.book_id not in self.saved_books:
                recommended_books.append(f'ID {book.book_id}: {book.title}')

        return recommended_books

    def get_saved_books(self) -> list[str]:
        """Return a list of id + title for the list of saved books."""
        saved_books = []

        for book_id in self.saved_books:
            book = self.books[book_id]
            saved_books.append(f'ID {book.book_id}: {book.title} (saved book)')

        return saved_books

    def get_similar_books(self) -> list[str]:
        """Return a list of ID and title for the list of similar books."""
        similar_books = []

        for book_id in self.similar_books:
            book = self.books[book_id]
            similar_books.append(f'ID {book.book_id}: {book.title} (similar book)')

        return similar_books

    def update_book_status(self) -> None:
        """Generate saved books and similar books (using saved books)."""
        try:
            with open('data/book.txt', 'r+') as file:
                lines = file.readlines()
                saved_books = {int(line.strip('\n')) for line in lines if int(line.strip('\n')) in self.books}
        except FileNotFoundError:
            saved_books = {}

        self.saved_books = saved_books
        self.similar_books = {book for book in self.sim_sys.recommend(saved_books) if book in self.books}

    def get_book_info(self) -> str:
        """Return the full information of the chosen book."""
        book = self.books[self.current_book]

        return 'Title: ' + book.title + '\n\nAuthor(s): \n' \
            + ''.join(['- ' + book.authors[author] + '\n' for author in book.authors]) + '\nGenre(s): \n' \
            + ''.join(['- ' + genre + '\n' for genre in book.genres]) \
            + '\nCountry: ' + book.country + '\nLanguage: ' + book.language + '\n\nNumber of pages: ' \
            + str(book.num_pages) + '\n\nAverage rating: ' + str(book.average_rating) + '\nRating count: ' \
            + str(book.ratings_count) + '\n\nDescription: \n\n' + book.description + '\n\nLink: ' + book.link

    def save_book_id(self) -> None:
        """Save book ID by writing it to file."""
        if self.current_book == 0:
            dialog = QMessageBox()
            dialog.setText('Please select a book (using the search button).')
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
            dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
            dialog.setWindowTitle('Warning!')
            dialog.exec()
        else:
            try:
                with open('data/book.txt', 'r+') as file:
                    lines = file.readlines()
                    book = str(self.current_book)
                    if book not in [line.strip('\n') for line in lines]:
                        file.write(book + '\n')
            except FileNotFoundError:
                with open('data/book.txt', 'w+') as file:
                    book = str(self.current_book)
                    file.write(book + '\n')
            finally:
                dialog = QMessageBox()
                dialog.setText('This book has been saved.')
                dialog.setIcon(QMessageBox.Icon.Information)
                dialog.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
                dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
                dialog.setWindowTitle('Successful!')
                dialog.exec()

                self.similar_books_search()

    def unsave_book_id(self) -> None:
        """Unsave book ID by removing it from file."""
        if self.current_book == 0:
            dialog = QMessageBox()
            dialog.setText('Please select a book (using the search button).')
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
            dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
            dialog.setWindowTitle('Warning!')
            dialog.exec()
        else:
            try:
                with open('data/book.txt', 'r+') as file:
                    book = str(self.current_book)
                    lines = [line.strip('\n') for line in file.readlines() if line.strip('\n') != book]
            except FileNotFoundError:
                dialog = QMessageBox()
                dialog.setText('No books have yet been saved.')
                dialog.setIcon(QMessageBox.Icon.Warning)
                dialog.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
                dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
                dialog.setWindowTitle('Warning!')
                dialog.exec()
            else:
                with open('data/book.txt', 'w+') as file:
                    file.writelines([line + '\n' for line in lines])

                dialog = QMessageBox()
                dialog.setText('This book has been unsaved.')
                dialog.setIcon(QMessageBox.Icon.Information)
                dialog.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
                dialog.setDefaultButton(QMessageBox.StandardButton.Ok)
                dialog.setWindowTitle('Successful!')
                dialog.exec()

                self.similar_books_search()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['forbidden-import', 'undefined-variable', 'wildcard-import',
                    'too-many-instance-attributes', 'too-many-locals', 'too-many-statements',
                    'too-many-branches', 'forbidden-IO-function']
    })
