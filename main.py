from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


class ChromeOptionsManager:
    def _init_(self):
        pass
    def get_options(self) -> Options:
        options = webdriver.ChromeOptions()
        return options


class ChromeDriverManager:
    def _init_(self, options: Options):
        self.options = options

    def get_driver(self) -> webdriver.Chrome:
        return webdriver.Chrome(options=self.options)


class WebsiteNavigator:
    def _init_(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self.url = url

    def go_to_website(self):
        self.driver.get(self.url)
        time.sleep(10)


class DataScraper:
    def _init_(self, driver: webdriver.Chrome):
        self.driver = driver
        self.data = []

    def scrape_data(self, start: int, end: int):
        for i in range(start, end):
            entry = self._scrape_entry(i)
            if entry:
                self.data.append(entry)
            time.sleep(10)

    def _scrape_entry(self, index: int):
        try:
            self.driver.find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[{index}]').click()
            time.sleep(10)
            name = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1').text
            address, phone, pluscode = self._scrape_details()
            links = self._scrape_links()
            return [name, address, phone, pluscode, links]
        except NoSuchElementException:
            return None

    def _scrape_details(self):
        details = []
        for a in range(1, 15):
            for b in range(1, 15):
                try:
                    details.append(self.driver.find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[{a}]/div[{b}]/button/div/div[2]/div[1]').text)
                except NoSuchElementException:
                    pass
        address = details[0]
        phone = details[1] if details[1].startswith('+') else details[2]
        pluscode = details[2] if details[1].startswith('+') else details[3]
        return address, phone, pluscode

    def _scrape_links(self):
        links = []
        for x in range(3, 9):
            for y in range(9, 13):
                try:
                    element = self.driver.find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[{y}]/div[{x}]/a')
                    links.append(element.get_attribute('href'))
                except NoSuchElementException:
                    pass
        return links


class DataSaver:
    @staticmethod
    def save_to_excel(data, file_name='veriler.xlsx'):
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False, header=False)


def main():
    options_manager = ChromeOptionsManager()
    chrome_options = options_manager.get_options()

    driver_manager = ChromeDriverManager(options=chrome_options)
    driver = driver_manager.get_driver()

    navigator = WebsiteNavigator(driver, url="")
    navigator.go_to_website()

    scraper = DataScraper(driver)
    scraper.scrape_data(start=1, end=4938)

    DataSaver.save_to_excel(scraper.data)


if _name_ == '_main_':
    main()