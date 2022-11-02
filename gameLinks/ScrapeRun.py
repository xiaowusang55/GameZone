from gameLinks.LinkSpider import LinkSpider

if __name__ == '__main__':

    # find all links and save
    driver = LinkSpider(
        url='https://ku.gamersky.com/sp/',
        selector='.imglist.pageContainer',
        save_dir_path='/Users/wukailang/Documents/GameZoneFiles/linksListFiles/')
    driver.run()
    driver.auto_next_page(750)
