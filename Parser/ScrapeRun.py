import os
import re
import datetime
import uuid

from Parser import Parser
import mysql.connector


if __name__ == '__main__':
    # create a parser
    lp = Parser()
    """
    extract data need
    game detail link,
    game cover link,
    game rates,
    game name
    """
    regx = r"""
        <a\s
        (href=.*?)\s.*?>       # find href attribute with () group
        <img\s(src=.*?)\s.*?>  # find src attribute with () group
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
    dbms = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='game_zone'
    )
    # create cursor
    mycursor = dbms.cursor()

    # create table
    # mycursor.execute('CREATE TABLE game_links (id INT AUTO_INCREMENT PRIMARY KEY, game_id VARCHAR(225), detail_url VARCHAR(225), cover_url VARCHAR(225), game_rate VARCHAR(225), game_name VARCHAR(225), created_time DATETIME, updated_time DATETIME)')

    sql = 'INSERT INTO game_links (game_id, detail_url, cover_url, game_rate, game_name, created_time, updated_time) VALUES (%s, %s, %s, %s, %s, %s, %s)'

    # parse the file in a loop and save it to db
    for file_path in original_order_list:
        lp.parse(full_path=file_path, reg=regx)
        for (detail_url, cover_url, game_rate, game_name) in lp.result:
            val = (str(uuid.uuid4()), detail_url, cover_url, game_rate, game_name, datetime.datetime.now(), datetime.datetime.now())
            mycursor.execute(sql, val)
            dbms.commit()

    dbms.close()
