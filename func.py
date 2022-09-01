from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import chromedriver_autoinstaller
from time import sleep
from FB2 import FictionBook2, Author
import requests


class AuthorToday:

    def __init__(self, url):
        self.url = url
        self.driver = self.selenium_setup()
        self.book_info = self.get_book_info()
        self.text_book = self.get_text_book()
        self.create_fb2()

    @staticmethod
    def selenium_setup():
        """
        Устанавливает и возвращает драйвер selenium
        :return: selenium.webdriver.chrome.webdriver.WebDriver
        """
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome()
        return driver

    def get_book_info(self):
        driver = self.driver
        driver.get(self.url)
        title = driver.find_element(By.CLASS_NAME, 'book-title').text
        author = driver.find_element(By.CLASS_NAME, 'book-authors').text
        author_home_page = driver.find_element(
            By.XPATH,
            '//*[@id="pjax-container"]/section/div/div/div[1]/div[1]/div/div/div[2]/div[1]/span/a').get_attribute(
            'href')
        genres = driver.find_element(By.CLASS_NAME, 'book-genres').text
        annotation = driver.find_element(By.CLASS_NAME, 'annotation').text
        img = driver.find_element(By.CLASS_NAME, 'cover-image').get_attribute('src')
        fb2_info = {'title': title, 'author': author, 'genres': genres.split(','), 'annotation': annotation, 'img': img,
                    'author_home_page': author_home_page}
        return fb2_info

    def get_chapter(self):
        driver = self.driver
        title = driver.find_element(By.TAG_NAME, 'h1').text
        paragraph = [i.text for i in driver.find_elements(By.TAG_NAME, 'p')]
        print(f'{title}')
        return title, paragraph

    def get_text_book(self):
        chapters = []
        driver = self.driver
        driver.get(self.url.replace('work', 'reader'))
        btn = driver.find_element(By.XPATH, '//*[@id="reader"]/div[2]/div/ul/li/a')

        while True:
            try:
                chapters.append(self.get_chapter())
            except NoSuchElementException:
                sleep(1)
                chapters.append(self.get_chapter())
            try:
                btn.click()
            except StaleElementReferenceException:
                print('Закончили')
                break
        return chapters

    def create_fb2(self):
        book = FictionBook2()
        book.titleInfo.title = self.book_info['title']
        book.titleInfo.annotation = self.book_info['annotation']
        book.titleInfo.authors = [Author(firstName=self.book_info['author'],
                                         homePages=[self.book_info['author_home_page']])]
        book.titleInfo.genres = self.book_info['genres']
        book.titleInfo.coverPageImages = [
            requests.get(self.book_info['img']).content]
        book.documentInfo.authors = self.book_info['author']
        book.documentInfo.version = "1.1"
        book.chapters = self.text_book
        book.write(f'{self.book_info["title"]}.fb2')


def main():
    at = AuthorToday('https://author.today/work/210008')


if __name__ == '__main__':
    main()
