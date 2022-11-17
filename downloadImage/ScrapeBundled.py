import shutil  # save img locally

import mysql.connector
import requests  # request img from web
from tqdm import tqdm


# DBmsConnect
class DBmsConnect:

    def __init__(self):
        self.dbms = mysql.connector.connect(
            host='1.12.59.12',
            user='xws',
            password='Yanzi@520',
            database='game_zone'
        )


# FileMaker
class FileMaker:

    def __init__(self, full_path, mode, encoding='utf-8'):
        self.full_path = None
        self.mode = None
        self.content = None
        try:

            self.file = open(full_path, mode)
        except Exception as e:
            print('File creation failed!')
            print(e)

    def write(self, content):
        self.file.write(content)
        self.file.close()
        print(f'{self.file.name} creation succeed!')

    def read(self):
        self.content = self.file.read()
        self.file.close()
        print(f'{self.file.name} read succeed!')


# connect dbms
dbms = DBmsConnect().dbms
cursor = dbms.cursor()
# query data from game_links table
cursor.execute('SELECT * FROM game_links')
data = cursor.fetchall()

# scrape detail page in for loop
for index in tqdm(range(len(data))):
    (id, game_id, detail_url, cover_url, game_rate, game_name, created_time, updated_time) = data[index]
    res = requests.get(cover_url, stream=True)
    # save the source page to local txt file
    file_name = f'{game_id}'
    fm = FileMaker(f'/home/xws/static/images/game-zone/{file_name}.jpg', 'wb')
    shutil.copyfileobj(res.raw, fm.file)
