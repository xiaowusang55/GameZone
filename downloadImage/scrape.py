import shutil  # save img locally
from tqdm import tqdm

import requests  # request img from web

from utils.DBmsConnect import DBmsConnect
from utils.FileMaker import FileMaker

# connect dbms
dbms = DBmsConnect().dbms
cursor = dbms.cursor()
# query data from game_links table
cursor.execute('SELECT * FROM game_links')
data = cursor.fetchall()
data = data[:1]

# scrape detail page in for loop
for index in tqdm(range(len(data))):
    (id, game_id, detail_url, cover_url, game_rate, game_name, created_time, updated_time) = data[index]
    res = requests.get(cover_url, stream=True)
    # save the source page to local txt file
    file_name = f'{id}_{game_name}_{game_id}'
    fm = FileMaker(f'/Users/wukailang/Documents/GameZoneImages/{file_name}.jpg', 'wb')
    shutil.copyfileobj(res.raw, fm.file)
