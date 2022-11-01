import random
import time

from selenium.webdriver.common.by import By

from gameLinks.Seleniumer import Seleniumer
from utils.FileMaker import FileMaker


class LinkSpider:

    def __init__(self, url, selector, save_dir_path):
        """
        :param url: the web url you want to scrape
        :param selector: which part of the web page you want to scrape
        :param save_dir_path: where to save the scraped contents
        """
        self.driver = Seleniumer().driver
        self.url = url
        self.content = None
        self.selector = selector
        self.save_dir_path = save_dir_path

    def find_page_num_and_create_txt(self):
        # get current page number
        page_num = self.driver.find_element(By.CSS_SELECTOR, '#pe100_page_pictxt a.p3').text
        file_name = f'第{page_num}页'

        # save the source page to local txt file
        fm = FileMaker(f'{self.save_dir_path}{file_name}.txt', 'w')
        fm.write(self.content)

    def get_list_container(self):
        js_script = """
                   return document.querySelector(arguments[0]).outerHTML
                   """
        self.content = self.driver.execute_script(js_script, self.selector)

        # save the first page
        self.find_page_num_and_create_txt()

    def run(self):
        # open the web page
        self.driver.get(self.url)

        # sleep for 3sec
        time.sleep(3)

        # get the list container
        self.get_list_container()

    def auto_next_page(self, times):
        """
        automate next page click
        :param times
        :return None
        """
        for num in range(times):
            # random sleep from 5 to 10 secs
            time.sleep(random.randint(5, 10))

            next_btn = self.driver.find_element(By.CSS_SELECTOR, '#pe100_page_pictxt a.p1.nexe')
            if bool(next_btn):
                next_btn.click()

                # sleep for 3sec
                time.sleep(3)

                # get the list container
                self.get_list_container()


if __name__ == '__main__':
    driver = LinkSpider(url='https://ku.gamersky.com/sp/', selector='.imglist.pageContainer',
                        save_dir_path='/Users/wukailang/Desktop/GameZone/files/linksListFiles/'
                        )
    time.sleep(3)
    driver.run()
