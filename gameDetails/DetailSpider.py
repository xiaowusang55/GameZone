import random
import time

from utils.DBmsConnect import DBmsConnect
from utils.FileMaker import FileMaker
from utils.Seleniumer import Seleniumer


class DetailSpider:

    def __init__(self, save_dir_path):
        self.driver = Seleniumer().driver
        self.save_dir_path = save_dir_path

    def run(self):
        # connect dbms
        dbms = DBmsConnect().dbms
        cursor = dbms.cursor()
        # query data from game_links table
        cursor.execute('SELECT * FROM game_links LIMIT 500 OFFSET 720')
        data = cursor.fetchall()

        # scrape detail page in for loop
        for (id, game_id, detail_url, cover_url, game_rate, game_name, created_time, updated_time) in data:
            self.driver.get(detail_url)
            time.sleep(3)
            # save the source page to local txt file
            file_name = f'{id}_{game_name}_{game_id}'
            fm = FileMaker(f'{self.save_dir_path}{file_name}.txt', 'w')
            fm.write(self.driver.page_source)
            time.sleep(random.randint(10, 15))


if __name__ == '__main__':
    ds = DetailSpider(save_dir_path='/Users/wukailang/Documents/GameZoneFiles/detailFiles/')
    ds.run()
