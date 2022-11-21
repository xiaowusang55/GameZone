from tqdm import tqdm

from utils.DBmsConnect import DBmsConnect

# connect to mysql
dbms = DBmsConnect().dbms
# create cursor
cursor = dbms.cursor()

# query data from game_links table
cursor.execute('SELECT * FROM game_links')
data = cursor.fetchall()

for i in tqdm(range(len(data))):
    sql = "UPDATE game_links SET id = %s where game_id = %s"
    val = (i + 1, data[i][1])
    cursor.execute(sql, val)
    dbms.commit()
dbms.close()
