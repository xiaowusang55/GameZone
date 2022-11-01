from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Seleniumer:
    """
        only support Chrome for now
    """

    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


if __name__ == '__main__':
    driver = Seleniumer().driver
    driver.get('https://baidu.com')
    print(driver.page_source)
