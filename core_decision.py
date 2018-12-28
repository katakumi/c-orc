# -*- coding: utf-8 -*-

from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
import json
import redis
import mysql.connector
from datetime import datetime
from pyknow import *

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='takumi',
    database='test',
)
cursor = conn.cursor()

# データベース「test」を選択
cursor.execute("USE test")
conn.commit()

class ResourceConnectorAgent(EdgeBaseAgent):
    #
    ACTIONS = {
        'OUTPUT': 'act_output',
        # 'TIME' : 'act_time'
    }

    # def act_time(self, msg: AgentMessage):
    #     # sql2 = "UPDATE iot_table SET Practically = 2 WHERE Task_name = 'aa';"
    #     # cursor.execute(sql2)
    #     # conn.commit()
    #     print("aaa")




    def act_output(self, msg: AgentMessage):


        # メッセージ関連
        # --------------------------------
        print(">>>", msg.Args)
        # msg.Args["decison"] = data  # 辞書の追加
        msg.To = "Operation"  # 宛先の変更
        # msg.From = "Decison"
        agt.send_message(msg, qos=0)  # メッセージ送信
        # --------------------------------


        # mysql関連
        # --------------------------------
        insert_iot = "INSERT INTO iot_table (Task_Name, WCAs, start_unix, end_unix, wap, Priority, type, Practically) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        # val = (Task_Name, WCAs, start_unix, end_unix, Priority, Type)
        val = (msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"], msg.Args["end_unix"], msg.Args["wap"], msg.Args["Priority"],msg.Args["Type"],msg.Args["Priority"])
        cursor.execute(insert_iot, val)
        conn.commit()
        # --------------------------------


        now = datetime.now()
        # print(now)
        now_unix = now.timestamp()
        # print(now_unix)
        now_unix = now_unix
        after_unix = now_unix + 300
        # print(now_unix)



        # 5分毎の処理
        sql = "SELECT * FROM iot_table WHERE Start_unix > '%s' AND Start_unix < '%s';"
        cursor.execute(sql, (now_unix, after_unix))
        result = cursor.fetchall()
        cursor.nextset()
        # conn.commit()
        print("result------", result)
        data = {}
        n = 0
        for r in result:
            data[n] = r
            print(r)
            n += 1
        # conn.close()



        # if data[0][4] > data[1][4]:
        #     # 結果の反映
        #     # sql2 = "UPDATE iot_table SET Practically = 2 WHERE Task_name = 'aa';"
        #     sql2 = "UPDATE iot_table SET Practically = 2 WHERE Task_name = '%s':"
        #     cursor.execute(sql2, data[0][0])
        #     print("aaaaaa")
        # elif data[0][4] < data[1][4]:
        #     sql2 = "UPDATE iot_table SET Practically = 2 WHERE Task_name = '%s':"
        #     # cursor.execute(sql2, data[1][0])
        #     print("bbbbbb")
        # elif data[0][4] == data[1][4]:
        #     if data[0][6] > data[1][6]:
        #         sql2 = "UPDATE iot_table SET Practically = 2 WHERE Task_name = '%s':"
        #         cursor.execute(sql2, data[0][0])
        #         print("cccc")
        #     elif data[0][6] < data[1][6]:
        #         sql2 = "UPDATE iot_table SET Practically = 2 WHERE Task_name = '%s':"
        #         cursor.execute(sql2, data[1][0])
        #         print("dddd")
        #     else :
        #         print("eeeeee")
        conn.commit()


        # sql = "update iot_table set Practically = 2 where Task_name = 'aa';"
        # cursor.execute(sql)
        # result = cursor.fetchall()
        # print(result)

        # sql2 = "UPDATE iot_table SET Practically = 2 WHERE Task_name = 'aa';"
        # cursor = conn.cursor(buffered=True)
        # cursor.execute(sql2)
        # conn.commit()

    # --------------------------------



        # print(r.keys())  # redisに保存されているkeyの一覧取得
        # redisに保存されているデータ取得
        # r.set(msg.Date, msg.Args)


        # 現在のunixtimeを取得
        # 現在時刻で設定されているIoTアプリはないかDBを検索
        # 複数個登録されていたら優先度を比較
        # 優先度によって経路を変更
        # DBにIoTアプリが使用するWAPの情報を優先度によって書き込む
        #






if __name__ == "__main__":
    print("===============================================================")
    print("OUTPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : Ctrl-c")
    # エージェントの起動
    agt = ResourceConnectorAgent("Decision", local=True)
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushall()  # redisに保存されているキーすべて消去
    # テーブル「wca_table」の消去 (プログラム起動時に実行させる）
    sql = "DROP TABLE  IF EXISTS iot_table"
    cursor.execute(sql)

    # テーブル「wca_table」を作成
    cursor.execute("""CREATE TABLE IF NOT EXISTS iot_table(
                    # id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                    Task_Name VARCHAR(10),
                    WCAs VARCHAR(5),
                    Start_unix INT,
                    End_unix INT,
                    WAP INT,
                    Priority INT,
                    WCA INT,
                    Type INT,
                    Practically INT);""")
    conn.commit()

    now = datetime.now()
    now_unix = now.timestamp()


    # defaultデータ
    insert_iot = "INSERT INTO iot_table (Task_Name, WCAs, Start_unix, End_unix, WAP, Priority, Type, Practically) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    Task_Name = 'aa'
    WCAs = 'b'
    Start_unix = now_unix + 60
    End_unix = now_unix + 6000
    wap = 1
    Priority = 0
    Type = 0
    Practically = 0
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Practically)
    cursor.execute(insert_iot, val)
    conn.commit()

    Task_Name = 'bb'
    WCAs = 'b'
    Start_unix = now_unix + 100
    End_unix = now_unix + 1000
    wap = 1
    Priority = 1
    Type = 1
    Practically = 0
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Practically)
    cursor.execute(insert_iot, val)
    conn.commit()

    Task_Name = 'cc'
    WCAs = 'b'
    Start_unix = now_unix + 50000
    End_unix = now_unix + 60000
    wap = 1
    Priority = 2
    Type = 2
    Practically = 0
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Practically)
    cursor.execute(insert_iot, val)
    conn.commit()

    Task_Name = 'dd'
    WCAs = 'b'
    Start_unix = now_unix + 1000
    End_unix = now_unix + 5000
    wap = 1
    Priority = 2
    Type = 2
    Practically = 0
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Practically)
    cursor.execute(insert_iot, val)
    conn.commit()

    print("AAA")
