from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import chromedriver_autoinstaller
from time import sleep


class AuthorToday:

    def __init__(self, url):
        self.url = url
        self.driver = self.selenium_setup()

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
        genres = driver.find_element(By.CLASS_NAME, 'book-genres').text
        annotation = driver.find_element(By.CLASS_NAME, 'annotation').text
        fb2_info = {'title': title, 'author': author, 'genres': genres, 'annotation': annotation}
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


def main():
    at = AuthorToday('https://author.today/work/210008')
    text = at.get_text_book()
    print(*text)


if __name__ == '__main__':
    main()
