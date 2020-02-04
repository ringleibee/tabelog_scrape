from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import sqlite3
from contextlib import closing

 #食べログ文回す (完成したら60にする)
for i in range(1, 3):
    url = "https://tabelog.com/tokyo/rstLst/lunch/" + str(i) + "/?LstSmoking=0&svd=20200204&svt=1900&svps=2&LstCosT=1&RdoCosTp=1"
    
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    bs = BeautifulSoup(response.text, 'html.parser')

 #店舗名取得
    titles = bs.find_all(class_="list-rst__rst-name-target")
 #店舗URL取得
    links = bs.find_all("href")

 #SQLにInsertするため、店舗名と店舗URLを結合しタプルのリスト化
    tupleOfList = []
    for contents in titles:

        # 第一引数は店舗、第二引数はURL
        content = (contents.text, contents.get('href'),)
        tupleOfList.append(content)
    
 #SQlite
dbname =  'database.db'
        
with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()

    drop_table = "DROP TABLE IF EXISTS tabelogs"
    create_table = '''create table tabelogs (id integer primary key autoincrement, name varchar(64), url text)'''
    c.execute(drop_table)
    c.execute(create_table)

    sql= 'insert into tabelogs (name, url) values (?, ?)'
    content = tupleOfList
    c.executemany(sql, tupleOfList)


    # 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
    # executemanyメソッドを実行する
    # insert_sql = 'insert into users (id, name, age, gender) values (?,?,?,?)'
    # users = [
    #     (2, 'Shota', 54, 'male'),
    #     (3, 'Nana', 40, 'female'),
    #     (4, 'Tooru', 78, 'male'),
    #     (5, 'Saki', 31, 'female')
    # ]
    # c.executemany(insert_sql, users)
    conn.commit()

    select_sql = 'select * from tabelogs'
    for row in c.execute(select_sql):
        print(row)
