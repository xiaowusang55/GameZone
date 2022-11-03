import datetime
import os
import pprint
import re
import uuid

from dataModel.GameDetailDM import GameDetailDM
from utils.DBmsConnect import DBmsConnect
from utils.MatchTxt import Matcher


def parse_game_links():
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
    files_counts = os.listdir('/Users/wukailang/Documents/GameZoneFiles/linksListFiles')
    # keep the order
    original_order_list = list(range(len(files_counts) - 1))
    for root, dirs, files in os.walk('/Users/wukailang/Documents/GameZoneFiles/linksListFiles'):
        for file in files:
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


def parse_game_detail():
    pass


if __name__ == '__main__':
    # parse links test
    # regxe = r"""
    # <a\s
    # href="(.*?)"\s.*?>       # find href attribute with () group
    # <img\ssrc="(.*?)"\s.*?>  # find src attribute with () group
    # <div\s.*?>(.*?)</div>  # find contents of tag with () group
    # <p>(.*?)</p>           # find contents of tag with () group
    # </a>
    # """
    # lp.parse(full_path='/Users/wukailang/Documents/GameZoneFiles/linksListFiles/第1页.txt', reg=regxe)
    # pprint.pprint(lp.result[0])

    # parse details test
    # 2_使命召唤19现代战争2_bd8606cd-f88c-40cf-933e-9210cd48e489.txt
    # 1_猎天使魔女3_8ccdfe16-5e50-49e1-bc6d-bb7315d08445.txt
    matcher = Matcher(
        full_path='/Users/wukailang/Documents/GameZoneFiles/detailFiles/1_猎天使魔女3_8ccdfe16-5e50-49e1-bc6d-bb7315d08445.txt')

    game_cn_name_reg = r"""<div\sclass="tit_CH"\s.*?>(.*?)</div>"""
    game_original_name_reg = r"""<div\sclass="tit_EN".*?>(.*?)</div>"""
    game_total_story_time_reg = r"""<div.*?title="游戏时长">(.*?)</div>"""

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
    game_type = f'{game_type_result.group(1)}_{game_type_result.group(2)}'

    game_is_cn_supported_and_producer_reg = r"""
    <div\sclass="tt[0-9]">
    <div\sclass="tit">(.*?)：</div>
    <div\sclass="txt">(.*?)</div>
    </div>
    """

    game_desc_reg = r"""
    <div\sclass="con-hide">
    \n\s*                 # handle newline and space
    <p>\u3000*(.*)</p>
    \s*\n\s*              # handle newline and space
    </div>
    """

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
        game_total_story_time=matcher.re_search(game_total_story_time_reg).group(1),
        game_release_date_and_platform=game_release_date_and_platform,
        game_type=game_type,
        game_is_cn_supported=matcher.re_findall(game_is_cn_supported_and_producer_reg)[0][1],
        game_producer=matcher.re_findall(game_is_cn_supported_and_producer_reg)[1][1],
        game_desc=matcher.re_search(game_desc_reg).group(1),
        game_player_tags=game_player_tags,
        game_pic_urls=matcher.re_findall(game_pic_urls_reg)
    )

    # pprint.pprint(matcher.re_findall(game_player_tags_reg))
    pprint.pprint(data_model.row)

