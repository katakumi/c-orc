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

# pyknow
# class RouteControl(KnowledgeEngine):
    # @Rule(Fact(rote="gw1-wap1"),(Fact(situation="ap1")))
    # def pattern1(self):
    #     print("aaa")
    #
    # @Rule(Fact(rote="gw2-wap2"),(Fact(situation="ap2")))
    # def pattern2(self):
    #     print("bbb")
    # @Rule(Fact(Start_unix=,WAP,Priority,Type)
    # def pattern1(self):
    #     print("aaa")
    #
    # @Rule(Fact(rote="gw2-wap2"),(Fact(situation="ap2")))
    # def pattern2(self):
    #     print("bbb")



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






        # HIから入力された情報の処理
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


        print(data[0][2])
        print(data[1][2])
        print("-------------")
        # 使用する時間とWAPが被っていたら
        if ((data[0][2] < data[1][2] and data[0][3] > data[1][2]) or \
            (data[0][2] > data[1][2] and data[0][2] < data[1][3]) or \
            (data[0][2] > data[1][2] and data[0][3] < data[1][3]) or \
            (data[0][2] < data[1][2] and data[0][3] > data[1][3])) and \
            (data[0][4] == data[1][4]):
                print("bbbbb")

                # pyknow
                # engine = RouteControl()
                # engine.reset()
                # engine.declare(
                #     Fact(WAP1=data[0][4]),
                #     Fact(Priority1=[0][5]),
                #     Fact(Type1=[0][6]),
                #     Fact(WAP2=data[1][4]),
                #     Fact(Priority2=[1][5]),
                #     Fact(Type2=[1][6])
                # )
                # engine.run()
        #ここでpyknow or business-ruleを使って優先度の比較処理とC-CONTへ送る経路変更の処理
        # 処理の結果、優先度と経路変更の情報を受け取る


        # HIから入力
        # 過去に入力されたアプリの要件と被っていないか比較
        # 結果を反映してデータベースへ保存
        #
        # C-CONTから経路情報を受け取る
        # 現在時刻でiot_tableを検索して優先させるアプリはないか
        #   現在時刻がstartのアプリを検索
        #   該当するWAPにそのアプリを利用するデバイスが存在
        #   他のアプリを利用しているが、同じgwを利用しているWAPがある
        #   関係ないアプリのWAPを他のGWへ接続するためのルール
        #
        #
        # あったらそのデバイスを優先させる処理
        # Operationへ送信

        # C-CONTから受け取る情報
        # 実際につながっているルート     rote(gw1-wap1,gw2-wap2)
        # 通信可能なルート              unused-rote(gw1-wap2,gw2-wap3)
        # デバイスが使用しているアプリ名 or IPアドレス     use-app(d1-aa,d2-aa,d3-bb)
        #
        data = {"rote":('gw1-wap1','gw2-wap2'), "unused-rote":("gw1-wap2","gw2-wap3") }







        # engine = RouteControl()
        # engine.reset()
        # # engine.declare(Fact(Light(data=str(input()))))
        # engine.declare(
        #     # Fact(rote=str(input("rote>>>"))),
        #     # Fact(situation=str(input("situation>>>"))),
        #     # Fact(AppPriority=int(input("AppPriority>>>")))
        #
        #     # Fact(Start_unix1=data[0][2]),
        #     Fact(WAP1=data[0][4]),
        #     Fact(Priority1=[0][5]),
        #     Fact(Type1=[0][6]),
        #     # Fact(Start_unix2=data[1][2]),
        #     Fact(WAP2=data[1][4]),
        #     Fact(Priority2=[1][5]),
        #     Fact(Type2=[1][6])
        # )
        # engine.run()



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

