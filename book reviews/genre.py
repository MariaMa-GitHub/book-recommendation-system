"""
Book Genre
"""

from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import csv


def extract_genre(url: str) -> list[str]:
    """
    Extract the genres of a book given the book url
    """

    # html_content = requests.get(url).text
    #
    # soup = BeautifulSoup(html_content, 'html.parser')
    #
    # items = soup.find_all('span', class_='BookPageMetadataSection__genreButton')
    # genres = [item.text for item in items]

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(5)
    elements = driver.find_elements(By.CSS_SELECTOR, 'span.BookPageMetadataSection__genreButton')

    return [element.text for element in elements]


if __name__ == '__main__':

    print(extract_genre('https://www.goodreads.com/book/show/22383541-primperfect'))

    print(extract_genre('https://www.goodreads.com/book/show/25421507-the-ticket'))

    # print(ha('https://www.goodreads.com/book/show/22383541-primperfect', extract_genres()))

    # print(ha('https://www.goodreads.com/book/show/25421507-the-ticket'))
