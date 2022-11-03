from parser.Parser import parse_game_links
from gameLinks.LinkSpider import LinkSpider

if __name__ == '__main__':

    # find all links and save
    driver = LinkSpider(
        url='https://ku.gamersky.com/sp/',
        selector='.imglist.pageContainer',
        save_dir_path='/Users/wukailang/Documents/GameZoneFiles/linksListFiles/')
    driver.run()
    driver.auto_next_page(750)

    # parse game links and save to db
    parse_game_links()
