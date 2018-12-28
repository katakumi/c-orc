import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='takumi',
    database='mysql',
)

cursor = conn.cursor()

# データベース「test」を選択
cursor.execute("USE test")
conn.commit()


# テーブル「wca_table」の消去 (プログラム起動時に実行させる）
sql = "DROP TABLE IF EXISTS wca_table"
cursor.execute(sql)


# テーブル「wca_table」を作成
cursor.execute("""CREATE TABLE IF NOT EXISTS wca_table(
                # id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                info VARCHAR(32),
                state INT);""")
conn.commit()


# データを挿入
insert_wca = "INSERT INTO wca_table (info, state) VALUES (%s, %s);"
# # 挿入するデータ
# wca_list = [
# ]
wca_list= [
    ('name','1'),
    ('State', '0'),
    ('INPUT', 100),
    ("OUTPUT", 200),
    ('rote1','19'),
    ('broken1','1')
]
# for文でまとめて書き込み
for state in wca_list:
    cursor.execute(insert_wca, state)

conn.commit()


# データを取得
cursor.execute('SELECT * FROM wca_table')
rows = cursor.fetchall()
# 出力
for i in rows:
    print(i)

dict = dict(rows)
print(type(dict))
print(dict)
print(dict["name"])

# # データを更新
# cursor.execute('UPDATE fruits_table SET value=1000 WHERE fruits="apple"')
# conn.commit()
# # データを取得
# cursor.execute('SELECT * FROM fruits_table')
# rows = cursor.fetchall()
# # 出力
# for i in rows:
#     print(i)


# # データを削除
# cursor.execute('DELETE FROM fruits_table WHERE fruits="melon"')
# conn.commit()
# # データを取得
# cursor.execute('SELECT * FROM wca_table')
# rows = cursor.fetchall()
# # 出力
# for i in rows:
#     print(i)
