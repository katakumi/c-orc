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

# テーブル「fruits_table」を作成
# cursor.execute("""CREATE TABLE IF NOT EXISTS fruits_table(
#                 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#                 fruits VARCHAR(32),
#                 value INT);""")
# conn.commit()


# データを挿入
insert_fruit = "INSERT INTO fruits_table (fruits, value) VALUES (%s, %s);"
# 挿入するデータ
fruit_list = [
    ("apple", 10),
    ("orange",20),
    ("melon", 500),
    ("pineapple", 700)
]
# for文でまとめて書き込み
for fruit in fruit_list:
    cursor.execute(insert_fruit, fruit)

conn.commit()


# # データを取得
# cursor.execute('SELECT * FROM fruits_table')
# rows = cursor.fetchall()
# # 出力
# for i in rows:
#     print(i)


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
# データを取得
cursor.execute('SELECT * FROM fruits_table')
rows = cursor.fetchall()
# 出力
for i in rows:
    print(i)