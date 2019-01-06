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
    ACTIONS = {
        'input_HI': 'act_HI',
        'OUTPUT_cognition': 'act_cognition',
        # 'TIME' : 'act_time'
    }

    # def act_time(self, msg: AgentMessage):
    #     # sql2 = "UPDATE iot_table SET Pecisive_pri = 2 WHERE Task_name = 'aa';"
    #     # cursor.execute(sql2)
    #     # conn.commit()
    #     print("aaa")
    def act_cognition(self, msg: AgentMessage):     # cognitionからの処理
        print(">>>",msg.Args)

    def write(self,taskname,wcas,startunix,endunix,wap,prirority1,type,prirority2):
        insert_iot = "INSERT INTO iot_table (Task_Name, WCAs, start_unix, end_unix, wap, Priority, type, Pecisive_pri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        val = (taskname,wcas,startunix,endunix,wap,prirority1,type,prirority2)
        cursor.execute(insert_iot, val)
        conn.commit()
        # print("call write")

    def update(self,Pecisive_pri,Task_name):
        sql = "UPDATE iot_table SET Pecisive_pri = %s WHERE Task_name = %s ;"
        val = (Pecisive_pri,Task_name)
        cursor.execute(sql, val)
        conn.commit()

    def act_HI(self, msg: AgentMessage):            # HIからの処理

        print(">>>", msg.Args)
        # msg.Args["decison"] = data  # 辞書の追加

        # iot_tableにデータが入っているか確認
        sql = "SELECT * FROM iot_table ;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.nextset()
        # conn.commit()
        print("result------", result)
        if len(result) == 0:        # iot_tableが空ならそのまま書き込み
            print("The database is empty")
            self.write(msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"], msg.Args["end_unix"],
                       msg.Args["wap"], msg.Args["Priority"], msg.Args["Type"], msg.Args["Priority"])
        else:
            #DBに保存されているデータを呼び出す処理
            # それを比較
            cursor.execute("SELECT * FROM iot_table;")
            result = cursor.fetchall()
            cursor.nextset()
            print(result)
            data = {}
            i = 0
            key = ["Task_Name", "WCAs", "start_unix", "end_unix","wap","Priority","type","Pecisive_pri"]
            for n in result:
                data[i] = dict(zip(key,n))
                # print(data[i])
                i += 1
            # if文で過去に入力されたデータと比較
            print("-----------------")
            i = 0
            flag = 0
            # 時間と優先度が被っていなかったらそのまま書き込み
            for n in data:
                if (((data[n]["start_unix"] < int(msg.Args["start_unix"]) and data[n]["end_unix"] > int(msg.Args["start_unix"])) or \
                    (data[n]["start_unix"] < int(msg.Args["end_unix"]) and data[n]["end_unix"] > int(msg.Args["end_unix"])) or \
                    (data[n]["start_unix"] > int(msg.Args["start_unix"]) and data[n]["end_unix"] < int(msg.Args["end_unix"])) or \
                    (data[n]["start_unix"] < int(msg.Args["start_unix"]) and data[n]["end_unix"] > int(msg.Args["end_unix"]))) and  \
                    (data[n]["Priority"] == int(msg.Args["Priority"]))):
                        print("same requirement ", data[n]["Task_Name"])
                        if data[n]["type"] < int(msg.Args["Type"]):         # タイプに優劣があったら実際の優先度変更
                            # self.write(msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"],msg.Args["end_unix"],
                            #            msg.Args["wap"], msg.Args["Priority"], msg.Args["Type"], 2)
                            self.update(data[n]["Pecisive_pri"]-1,data[n]["Task_Name"])
                        if data[n]["type"] == int(msg.Args["Type"]):
                            print("same condition ", data[n]["Task_Name"])


                        # flag = 1
                i += 1
            if flag == 0:
                self.write(msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"], msg.Args["end_unix"],
                       msg.Args["wap"], msg.Args["Priority"], msg.Args["Type"], msg.Args["Priority"])


                        # resultに入っている出力結果(list)を分解
            # dictにしたほうがif文でキーを使って比較できるから楽？
            # if文で今回入力されたアプリと時間・優先度が被っていないか比較
            # 被っていなければそのまま書き込み
            # 被っていてら優先度を再定義して書き込み
            # conn.commit()

            # if          # 時間と優先度が被っていなかったらそのまま書き込み
            # 時間が被っていないか
                #優先度が被っていないか
                    #
        # # mysql関連
        # # --------------------------------
        # insert_iot = "INSERT INTO iot_table (Task_Name, WCAs, start_unix, end_unix, wap, Priority, type, Pecisive_pri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        # # val = (Task_Name, WCAs, start_unix, end_unix, Priority, Type)
        # val = (msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"], msg.Args["end_unix"], msg.Args["wap"], msg.Args["Priority"],msg.Args["Type"],msg.Args["Priority"])
        # cursor.execute(insert_iot, val)
        # conn.commit()
        # # --------------------------------

        now = datetime.now()
        print(now)
        now_unix = now.timestamp()
        print(now_unix)
        now_unix = now_unix
        after_unix = now_unix + 300
        print(now_unix)


        # # HIから入力された情報の処理
        # sql = "SELECT * FROM iot_table WHERE Start_unix > '%s' AND Start_unix < '%s';"
        # cursor.execute(sql, (now_unix, after_unix))
        # result = cursor.fetchall()
        # cursor.nextset()
        # # conn.commit()
        # print("result------", result)
        # data = {}
        # n = 0
        # for r in result:
        #     data[n] = r
        #     print(r)
        #     n += 1
        # # conn.close()
        #
        #
        # print(data[0][2])
        # print(data[1][2])
        # print("-------------")
        # # 使用する時間とWAPが被っていたら
        # if ((data[0][2] < data[1][2] and data[0][3] > data[1][2]) or \
        #     (data[0][2] > data[1][2] and data[0][2] < data[1][3]) or \
        #     (data[0][2] > data[1][2] and data[0][3] < data[1][3]) or \
        #     (data[0][2] < data[1][2] and data[0][3] > data[1][3])) and \
        #     (data[0][4] == data[1][4]):
        #         print("bbbbb")
        #
        #
        # # engine = RouteControl()
        # # engine.reset()
        # # # engine.declare(Fact(Light(data=str(input()))))
        # # engine.declare(
        # #     # Fact(rote=str(input("rote>>>"))),
        # #     # Fact(situation=str(input("situation>>>"))),
        # #     # Fact(AppPriority=int(input("AppPriority>>>")))
        # #
        # #     # Fact(Start_unix1=data[0][2]),
        # #     Fact(WAP1=data[0][4]),
        # #     Fact(Priority1=[0][5]),
        # #     Fact(Type1=[0][6]),
        # #     # Fact(Start_unix2=data[1][2]),
        # #     Fact(WAP2=data[1][4]),
        # #     Fact(Priority2=[1][5]),
        # #     Fact(Type2=[1][6])
        # # )
        # # engine.run()
        #
        #
        #
        # # if data[0][4] > data[1][4]:
        # #     # 結果の反映
        # #     # sql2 = "UPDATE iot_table SET Pecisive_pri = 2 WHERE Task_name = 'aa';"
        # #     sql2 = "UPDATE iot_table SET Pecisive_pri = 2 WHERE Task_name = '%s':"
        # #     cursor.execute(sql2, data[0][0])
        # #     print("aaaaaa")
        # # elif data[0][4] < data[1][4]:
        # #     sql2 = "UPDATE iot_table SET Pecisive_pri = 2 WHERE Task_name = '%s':"
        # #     # cursor.execute(sql2, data[1][0])
        # #     print("bbbbbb")
        # # elif data[0][4] == data[1][4]:
        # #     if data[0][6] > data[1][6]:
        # #         sql2 = "UPDATE iot_table SET Pecisive_pri = 2 WHERE Task_name = '%s':"
        # #         cursor.execute(sql2, data[0][0])
        # #         print("cccc")
        # #     elif data[0][6] < data[1][6]:
        # #         sql2 = "UPDATE iot_table SET Pecisive_pri = 2 WHERE Task_name = '%s':"
        # #         cursor.execute(sql2, data[1][0])
        # #         print("dddd")
        # #     else :
        # #         print("eeeeee")
        # conn.commit()

        msg.To = "Operation"  # 宛先の変更
        agt.send_message(msg, qos=0)  # メッセージ送信


        # sql = "update iot_table set Pecisive_pri = 2 where Task_name = 'aa';"
        # cursor.execute(sql)
        # result = cursor.fetchall()
        # print(result)

        # sql2 = "UPDATE iot_table SET Pecisive_pri = 2 WHERE Task_name = 'aa';"
        # cursor = conn.cursor(buffered=True)
        # cursor.execute(sql2)
        # conn.commit()

        # print(r.keys())  # redisに保存されているkeyの一覧取得
        # redisに保存されているデータ取得
        # r.set(msg.Date, msg.Args)


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
                    Pecisive_pri INT);""")
    conn.commit()

    now = datetime.now()
    now_unix = now.timestamp()


    # defaultデータ
    insert_iot = "INSERT INTO iot_table (Task_Name, WCAs, Start_unix, End_unix, WAP, Priority, Type, Pecisive_pri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    Task_Name = 'aa'
    WCAs = 'b'
    Start_unix = now_unix + 60
    End_unix = now_unix + 6000
    wap = 1
    Priority = 2
    Type = 0
    Pecisive_pri = Priority
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Pecisive_pri)
    cursor.execute(insert_iot, val)
    conn.commit()

    Task_Name = 'bb'
    WCAs = 'b'
    Start_unix = now_unix + 10
    End_unix = now_unix + 1000
    wap = 1
    Priority = 2
    Type = 1
    Pecisive_pri = Priority
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Pecisive_pri)
    cursor.execute(insert_iot, val)
    conn.commit()

    Task_Name = 'cc'
    WCAs = 'b'
    Start_unix = now_unix + 50
    End_unix = now_unix + 600
    wap = 1
    Priority = 2
    Type = 2
    Pecisive_pri = Priority
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Pecisive_pri)
    cursor.execute(insert_iot, val)
    conn.commit()

    # Task_Name = 'dd'
    # WCAs = 'b'
    # Start_unix = now_unix
    # End_unix = now_unix
    # wap = 1
    # Priority = 2
    # Type = 2
    # Pecisive_pri = Priority
    # val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Pecisive_pri)
    # cursor.execute(insert_iot, val)
    # conn.commit()

    print("AAA")

