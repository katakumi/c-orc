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
        now = datetime.now()
        now_unix = now.timestamp()
        sql = "SELECT Task_name, WAP, Pecisive_pri FROM iot_table WHERE Start_unix BETWEEN %s AND %s;"
        val = (now_unix, now_unix+180)
        cursor.execute(sql, val)             # 3分以内にstartするアプリを検索
        result = cursor.fetchall()
        conn.commit()
        processing_result = "no change"
        wap_name = "none"
        change = "none"
        device_name = "none"
        if len(result) != 0:
            print("3分以内に稼働するアプリ", result)       # Task_name, WAP, Pecisive_pri
            i = 0
            for n in result:
                if result[i][2] == 2:       # 優先度が２のアプリはないか
                    k = 0
                    flag = 0
                    for n in msg.Args["app_name"]:          # 優先度が2のアプリが使用されていなかったらbreak
                        if msg.Args["app_name"][k][3:] == result[i][0]:
                            flag = 1
                        k += 1
                    if flag == 0:
                        device_name = "unused"
                        break
                    print("優先度が2のアプリ", result[i])
                    j = 0
                    for n in msg.Args["route"]:
                        if msg.Args["route"][j][4:8] == "wap" + str(result[i][1]):
                            k = 0
                            for n in msg.Args["app_name"]:
                                if result[i][0] == msg.Args["app_name"][k][3:]:
                                    device_name = msg.Args["app_name"][k][0:2]
                                    print("優先度が2のアプリを使用しているデバイス",device_name)
                                    break
                                # else:
                                #     device_name = "unused"
                                k += 1
                            k = 0
                            for n in msg.Args["route"]:
                                if device_name == msg.Args["route"][k][9:]:     # 優先度の高いWAPが使用するGWを探す
                                    use_gw = msg.Args["route"][k][0:3]          # use_gw＝優先度が高いWAPが使用するGW
                                    print("優先度が高いWAPが使用しているGW", use_gw)
                                    break
                                k += 1
                            l = 0                                               # 他のWAPがuse_gwを使っていないか
                            for n in msg.Args["route"]:                         # wap_name=use_gwを使用している優先度が低いWAP
                                if (use_gw == msg.Args["route"][l][0:3]) and (device_name != msg.Args["route"][l][9:]):
                                    wap_name = msg.Args["route"][l][4:8]
                                    print("優先度が高いWAPと同じGWを使用しているWAP",wap_name)
                                    break
                                else:
                                    wap_name = "unused"
                                l += 1
                            if wap_name == "none":
                                break
                            k = 0
                            for n in msg.Args["unused_route"]:                  # wap_nameが使用できる未使用のroute
                                if wap_name == msg.Args["unused_route"][k][4:]:
                                    change = msg.Args["unused_route"][k]
                                    print("変更可能な未使用route",change)
                                    break
                                else:
                                    change = "unused"
                                k += 1
                            if change != "unused":
                                change_route = change + msg.Args["route"][l][8:]             # wap_nameの経路変更
                                print("変更後のroute", change_route)
                                msg.Args["route"][l] = change_route
                                processing_result = msg.Args["route"]
                        j += 1
                i += 1
            if wap_name == "none" and wap_name == "none" and device_name == "none":
                print("優先度が2のアプリなし")
            if device_name == "unused":
                print("優先度が高いアプリを使用しているデバイスなし")
            if wap_name == "unused" and change == "unused":
                print("優先度が高いWAPと同じGWを使用しているWAPなし")
            if change == "unused":
                print("変更可能な未使用のrouteなし")
        else:
            print("3分以内に稼働するアプリなし")
        msg.Args = processing_result
        print("結果",msg.Args)
        # print("wap name", wap_name)
        # print("device name", device_name)
        # print("change", change)

    def write(self,taskname,wcas,startunix,endunix,wap,prirority1,type,Pecisive_pri):
        insert_iot = "INSERT INTO iot_table (Task_Name, WCAs, start_unix, end_unix, wap, Priority, type, Pecisive_pri) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        val = (taskname,wcas,startunix,endunix,wap,prirority1,type,Pecisive_pri)
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
        # iot_tableにデータが入っているか確認
        sql = "SELECT * FROM iot_table ;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.nextset()
        # conn.commit()
        # print("result------", result)
        if len(result) == 0:        # iot_tableが空ならそのまま書き込み
            print("The database is empty")
            self.write(msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"], msg.Args["end_unix"],
                       msg.Args["wap"], msg.Args["Priority"], msg.Args["Type"], msg.Args["Priority"])
        else:       #DBに保存されているデータを呼び出し、それを比較
            cursor.execute("SELECT * FROM iot_table;")
            result = cursor.fetchall()
            cursor.nextset()
            # print(result)
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
            # 時間・優先度・WAPが被っていなかったらそのまま書き込み
            for n in data:
                if ((data[n]["start_unix"] < int(msg.Args["start_unix"] and data[n]["end_unix"] > int(msg.Args["start_unix"])) or \
                (data[n]["start_unix"] < int(msg.Args["end_unix"]) and data[n]["end_unix"] > int(msg.Args["end_unix"])) or \
                (data[n]["start_unix"] > int(msg.Args["start_unix"]) and data[n]["end_unix"] < int(msg.Args["end_unix"])) or \
                (data[n]["start_unix"] < int(msg.Args["start_unix"]) and data[n]["end_unix"] > int(msg.Args["end_unix"]))) and  \
                (data[n]["Priority"] == int(msg.Args["Priority"])) and (data[n]["wap"] == int(msg.Args["wap"]))):
                    if data[n]["type"] < int(msg.Args["Type"]):         # 保存されているアプリより入力されたアプリのほうが優先度が高いとき
                        # self.write(msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"],msg.Args["end_unix"],
                        #            msg.Args["wap"], msg.Args["Priority"], msg.Args["Type"], 2)
                        self.update(data[n]["Pecisive_pri"]-1,data[n]["Task_Name"])
                        print("same requirement ", data[n]["Task_Name"])
                    elif data[n]["type"] > int(msg.Args["Type"]):       # DBに保存してあるアプリの優先度のほうが高かったら、入力されたアプリの優先度を下げる
                        self.write(msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"],msg.Args["end_unix"],
                                   msg.Args["wap"], msg.Args["Priority"], msg.Args["Type"], int(msg.Args["Priority"])-1)
                        print("same requirement ", data[n]["Task_Name"])
                        flag = 1
                    elif data[n]["type"] == int(msg.Args["Type"]):          # 時間・優先度・WAP・タイプがすべて同じときはネットワークオペレータで処理をする(未実装)
                        print("same condition ", data[n]["Task_Name"])
                i += 1
            if flag == 0:       # 過去に入力されたアプリと要求が被っていなかったらそのまま保存
                self.write(msg.Args["Task Name"], msg.Args["WCAs"], msg.Args["start_unix"], msg.Args["end_unix"],
                       msg.Args["wap"], msg.Args["Priority"], msg.Args["Type"], msg.Args["Priority"])

        # now = datetime.now()
        # print(now)
        # now_unix = now.timestamp()
        # print(now_unix)
        # now_unix = now_unix
        # after_unix = now_unix + 300
        # print(now_unix)
        # msg.To = "Operation"  # 宛先の変更
        # agt.send_message(msg, qos=0)  # メッセージ送信

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
    Pecisive_pri = Priority -1
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Pecisive_pri)
    cursor.execute(insert_iot, val)
    conn.commit()

    Task_Name = 'bb'
    WCAs = 'b'
    Start_unix = now_unix + 60
    End_unix = now_unix + 20000
    wap = 3
    Priority = 2
    Type = 1
    Pecisive_pri = Priority
    val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Pecisive_pri)
    cursor.execute(insert_iot, val)
    conn.commit()
    #
    # Task_Name = 'cc'
    # WCAs = 'b'
    # Start_unix = now_unix + 40
    # End_unix = now_unix + 6000
    # wap = 1
    # Priority = 2
    # Type = 2
    # Pecisive_pri = Priority
    # val = (Task_Name, WCAs, Start_unix, End_unix, wap, Priority, Type, Pecisive_pri)
    # cursor.execute(insert_iot, val)
    # conn.commit()

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

