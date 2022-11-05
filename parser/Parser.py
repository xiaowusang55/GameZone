import datetime
import os
import re
import uuid

from dataModel.GameDetailDM import GameDetailDM
from utils.DBmsConnect import DBmsConnect
from utils.MatchTxt import Matcher
from bs4 import BeautifulSoup


def parse_game_links(dir_path):
    """
    extract data need
    game detail link,
    game cover link,
    game rates,
    game name
    """
    regx = r"""
            <a\s
            href="(.*?)"\s.*?>       # find href attribute with () group
            <img\ssrc="(.*?)"\s.*?>  # find src attribute with () group
            <div\s.*?>(.*?)</div>  # find contents of tag with () group
            <p>(.*?)</p>           # find contents of tag with () group
            </a>
            """

    # get the files number
    files_counts = os.listdir(dir_path)
    # keep the order
    original_order_list = list(range(len(files_counts) - 1))
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.txt'):
                num = re.search(r'\d{1,3}', file)
                # print(os.path.join(root, file))
                if num is not None:
                    original_order_list[int(num.group()) - 1] = os.path.join(root, file)

    # connect to mysql
    dbms = DBmsConnect().dbms
    # create cursor
    mycursor = dbms.cursor()

    # create table
    mycursor.execute(
        'CREATE TABLE game_links (id INT AUTO_INCREMENT PRIMARY KEY, game_id VARCHAR(225), detail_url VARCHAR(225), cover_url VARCHAR(225), game_rate VARCHAR(225), game_name VARCHAR(225), created_time DATETIME, updated_time DATETIME)')

    sql = 'INSERT INTO game_links (game_id, detail_url, cover_url, game_rate, game_name, created_time, updated_time) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    # parse the file in a loop and save it to db
    for file_path in original_order_list:
        mr = Matcher(full_path=file_path)
        result = mr.re_findall(reg=regx)
        for (detail_url, cover_url, game_rate, game_name) in result:
            val = (str(uuid.uuid4()), detail_url, cover_url, game_rate, game_name, datetime.datetime.now(),
                   datetime.datetime.now())
            mycursor.execute(sql, val)
            dbms.commit()

    dbms.close()


def parse_game_detail(dir_path):
    # get the files number
    files_counts = os.listdir(dir_path)
    # keep the order
    original_order_list = list(range(len(files_counts)))
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.txt'):
                mh = re.search(r'((\d)+)_.*?_((.*?-){4}.*?).txt',
                               file)  # 666_如龙3_fbce4a91-2301-4896-bdd9-91987448016d.txt
                num = mh.group(1)
                game_id = mh.group(3)
                full_path = os.path.join(dir_path, file)
                list_item = (game_id, full_path)
                if num is not None:
                    original_order_list[int(num) - 1000 - 1] = list_item

    # connect to mysql
    dbms = DBmsConnect().dbms
    # create cursor
    mycursor = dbms.cursor()

    # create table
    # mycursor.execute(
    #     'CREATE TABLE game_details \
    #         (id INT AUTO_INCREMENT PRIMARY KEY, \
    #         game_id VARCHAR(225), \
    #         game_cn_name VARCHAR(225), \
    #         game_original_name VARCHAR(225), \
    #         game_total_story_time VARCHAR(225), \
    #         game_release_date_and_platform TEXT, \
    #         game_type VARCHAR(225), \
    #         game_is_cn_supported VARCHAR(225), \
    #         game_producer VARCHAR(225), \
    #         game_desc LONGTEXT, \
    #         game_player_tags TEXT, \
    #         game_pic_urls TEXT, \
    #         created_time DATETIME, \
    #         updated_time DATETIME)'
    # )

    sql = 'INSERT INTO game_details \
        (game_id, \
        game_cn_name, \
        game_original_name, \
        game_total_story_time, \
        game_release_date_and_platform, \
        game_type, \
        game_is_cn_supported, \
        game_producer, \
        game_desc, \
        game_player_tags, \
        game_pic_urls, \
        created_time, \
        updated_time) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    # parse the file in a loop and save it to db
    for (game_id, full_path) in original_order_list:
        matcher = Matcher(full_path=full_path)

        game_cn_name_reg = r"""<div\sclass="tit_CH"\s.*?>(.*?)</div>"""
        game_original_name_reg = r"""<div\sclass="tit_EN".*?>(.*?)</div>"""
        game_total_story_time_reg = r"""<div.*?title="游戏时长">\s*?(.*?)\s*?</div>"""

        # handle game_release_date_and_platform data
        game_release_date_and_platform_reg = r"""<a.*?class="([a-zA-Z0-9]*)(\scur)?"\sdata-time="(.*?)">(.*?)</a>"""
        game_release_date_and_platform_result = matcher.re_findall(game_release_date_and_platform_reg)
        game_release_date_and_platform = []
        for (one, two, three, four) in game_release_date_and_platform_result:
            game_release_date_and_platform.append(f'{three}_{four}')

        game_type_reg = r"""
                <a\shref="http://ku.gamersky.com/sp/(.*?)/"\starget="_blank">(.*?)</a>
                """
        game_type_result = matcher.re_search(game_type_reg)
        game_type = f'{game_type_result.group(1)}_{game_type_result.group(2)}' if game_type_result is not None else ''

        game_is_cn_supported_and_producer_reg = r"""
                <div\sclass="tt[0-9]">
                <div\sclass="tit">(.*?)：</div>
                <div\sclass="txt">(.*?)</div>
                </div>
                """
        game_is_cn_supported_and_producer_result = matcher.re_findall(game_is_cn_supported_and_producer_reg)
        game_is_cn_supported = ''
        game_producer = ''
        for cn_and_producer in game_is_cn_supported_and_producer_result:
            if '官方中文' in cn_and_producer:
                game_is_cn_supported = cn_and_producer[1]
            elif '制作发行' in cn_and_producer:
                game_producer = cn_and_producer[1]

        # use re as possible as i can, but the desc text pattern is unknown so it is hard to
        # write a pattern that match all.
        # so to take a short path, use bs4 instead
        soup = BeautifulSoup(matcher.file.content, 'html.parser')
        game_desc_el = soup.find(class_="con-hide")
        game_desc = game_desc_el.text.strip()

        game_player_tags_reg = r"""
                <a\starget="_blank"\shref="http://ku.gamersky.com/sp/
                ((\d+-){5}\d+).html"  # match 0-0-0-79-0-0.html
                >(.*?)</a>"""
        game_player_tags_result = matcher.re_findall(game_player_tags_reg)
        game_player_tags = []
        for (one, two, three) in game_player_tags_result:
            game_player_tags.append(three)

        game_pic_urls_reg = r"""<a.*?data-pic="(.*?)".*?></a>"""

        data_model = GameDetailDM(
            game_cn_name=matcher.re_search(game_cn_name_reg).group(1),
            game_original_name=matcher.re_search(game_original_name_reg).group(1),
            game_total_story_time=matcher.re_search(game_total_story_time_reg).group(1).strip(),
            game_release_date_and_platform=','.join(game_release_date_and_platform),
            game_type=game_type,
            game_is_cn_supported=game_is_cn_supported,
            game_producer=game_producer,
            game_desc=game_desc,
            game_player_tags=','.join(game_player_tags),
            game_pic_urls=','.join((matcher.re_findall(game_pic_urls_reg)))
        )

        # parse the file in a loop and save it to db
        val = (game_id,) + data_model.row + (datetime.datetime.now(), datetime.datetime.now())
        mycursor.execute(sql, val)
        dbms.commit()

    dbms.close()
    print('Data import done!')


if __name__ == '__main__':
    # parse_game_detail(dir_path='/Users/wukailang/Documents/GameZoneFiles/detailFiles/1-1000/')
    parse_game_detail(dir_path='/Users/wukailang/Documents/GameZoneFiles/detailFiles/1001-2000/')
