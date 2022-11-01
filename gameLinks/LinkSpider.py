from selenium.webdriver.common.by import By

from gameLinks.Seleniumer import Seleniumer
from utils.FileMaker import FileMaker


class LinkSpider:

    def __init__(self, url):
        self.driver = Seleniumer().driver
        self.url = url

    def find_page_num_and_create_txt(self):
        # get current page number
        page_num = self.driver.find_element(By.CSS_SELECTOR, '#pe100_page_pictxt a.p3').text
        file_name = f'第{page_num}页'

        # save the source page to local txt file
        fm = FileMaker(f'/Users/wukailang/Desktop/GameZone/files/linksListFiles/{file_name}.txt', 'w')
        fm.write(self.driver.page_source)

    def run(self):
        # open the web page
        self.driver.get(self.url)

        # self.driver.execute_script("""console.log('haha')""")

        # save the first page
        # self.find_page_num_and_create_txt()


if __name__ == '__main__':
    LinkSpider('https://ku.gamersky.com').run()
