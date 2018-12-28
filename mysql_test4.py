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
sql = "DROP TABLE  IF EXISTS iot_table"
cursor.execute(sql)


# テーブル「wca_table」を作成
cursor.execute("""CREATE TABLE IF NOT EXISTS iot_table(
                # id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                Task_Name VARCHAR(10),
                WCAs VARCHAR(5),
                start_unix INT,
                end_unix INT,
                Priority INT,
                Type INT);""")
conn.commit()



Task_Namea = 'a'
WCAsa = 'b'
start_unixa = 1545106200.0
end_unixa = 1545109800.0
Prioritya = 0
Typea = 0

insert_iot = "INSERT INTO iot_table (Task_Name, WCAs, start_unix, end_unix, Priority, type) VALUES (%s, %s, %s, %s, %s, %s);"
val = (Task_Namea, WCAsa, start_unixa, end_unixa, Prioritya, Typea)
cursor.execute(insert_iot, val)
conn.commit()

#
# # データを挿入
# insert_iot = "INSERT INTO iot_table (info, state) VALUES (%s, %s);"
# # # 挿入するデータ
# iot_data = [
#     ('Task Name', 'a'),
#     ('WCAs', 'b'),
#     ('start_unix', 1545106200.0),
#     ('end_unix', 1545109800.0),
#     ('Priority', '0'),
#     ('Type', '0')
# ]
#
# # for文でまとめて書き込み
# for state in iot_data:
#     cursor.execute(insert_iot, state)
#
# conn.commit()
#
# # データを取得
# cursor.execute('SELECT * FROM iot_table')
# rows = cursor.fetchall()
# # 出力
# for i in rows:
#     print(i)
#
# dict = dict(rows)
# print(type(dict))
# print(dict)
# print(dict["Task Name"])


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
