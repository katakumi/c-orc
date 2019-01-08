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
        print("Current time search result")
        print("result", result)       # Task_name, WAP, Pecisive_pri
        # print("device_route", msg.Args["device_route"])
        # print(type(msg.Args["device_route"]))
        # print(type(result))
        # if len(msg.Args["device_route"]) < len(result):
        #     longer = result
        # elif len(msg.Args["device_route"]) > len(result):
        #     longer = msg.Args["device_route"]
        # else:
        #     longer = msg.Args["device_route"]
        # # print(longer)
        # i = 0
        # for n in longer:
        #     print("-----", result[i])
        #     if result[i][2] == 2:       # 現在時刻でstartするアプリの優先度が２だったら経路変更
        #         # print(msg.Args)
        #         print(result[i])
        #         # use_appで使われているアプリとRouteの中のデバイスが
        #         j = 0
        #         # if ("wap" + str(result[i][1])) == msg.Args["device_route"][0:3]
        #         print(msg.Args["device_route"][i][0:4])
        #
        #
        #
        #         # if "wap"+result[i][1]
        #         # j = 0
        #         # for n in msg.Args["app_name"]:
        #         #     if result[i][0] == msg.Args["app_name"][j][3:]:
        #         #         print("app_name",msg.Args["app_name"][j][3:])
        #     i += 1
        i = 0
        for n in result:
            if result[i][2] == 2:       # 優先度が２のアプリはないか
                print("優先度が2のアプリ", result[i])
                print("mark 1")
                j = 0
                # {'route': ('gw1-wap1-d1', 'gw2-wap2-d2', 'gw2-wap3-d3'), 'app_name': ('d1-aa', 'd2-aa', 'd3-bb'), 'unused_route': ('gw1-wap2', 'gw2-wap1')}
                for n in msg.Args["route"]:
                    print("mark 2")
                    print("route", msg.Args["route"])
                    print(msg.Args["route"][j][4:8])
                    if msg.Args["route"][j][4:8] == "wap" + str(result[i][1]):
                        print(msg.Args["route"][j][4:8], "wap" + str(result[i][1]))
                        k = 0
                        for n in msg.Args["app_name"]:
                            if result[i][0] == msg.Args["app_name"][k][3:]:
                                device_name = msg.Args["app_name"][k][0:2]
                                print("優先度が2のアプリを使用しているデバイス",device_name)
                                break
                            k += 1
                        # device_nameがあるRouteの中のGWを探す
                        k = 0
                        for n in msg.Args["route"]:
                            # print(msg.Args["route"][k][9:])
                            if device_name == msg.Args["route"][k][9:]:     # 優先度の高いWAPが使用するGWを探す
                                use_gw = msg.Args["route"][k][0:3]          # use_gw＝優先度が高いWAPが使用するGW
                                print("優先度が高いWAPが使用しているGW", use_gw)
                                break
                            k += 1
                        l = 0
                        for n in msg.Args["route"]:                         # 他のWAPがuse_gwを使っていないか
                            # print(msg.Args["route"][k][9:])               # wap_name=use_gwを使用している優先度が低いWAP
                            print(msg.Args["route"][l][0:3])
                            if (use_gw == msg.Args["route"][l][0:3]) and (device_name != msg.Args["route"][l][9:]):
                                wap_name = msg.Args["route"][l][4:8]
                                print("wap_name",wap_name)
                                break
                            l += 1
                        k = 0
                        for n in msg.Args["unused_route"]:                  # wap_nameが使用できる未使用のroute
                            # print(msg.Args["unused_route"][k][4:])        #
                            if wap_name == msg.Args["unused_route"][k][4:]:
                                change = msg.Args["unused_route"][k]
                                print("変更後のroute",change)
                                break
                            k += 1
                        # k = 0
                        # for n in msg.Args["route"]:                         # wap_nameの経路変更
                        #     if msg.Args["route"][k][4:8] == wap_name:
                        print(msg.Args["route"][l])
                        change_route = change + msg.Args["route"][l][8:]
                        print("変更後のroute", change_route)
                        msg.Args["route"][l] = change_route



                        # print(msg.Args["route"][j][9:], msg.Args["app_name"][k][3:])

                    # if msg.Args["app_name"][j][3:] == result[i][0]:      # 現在使われているデバイスの中で優先度が高いアプリを使用しているデバイスはないか
                        # print(msg.Args["app_name"][j])
                        # print(result[i])
                        # if msg.Args[]          # 優先度が高いアプリが指定されたWAPで使われているか
                    # if msg.Args["device_route"][j][0:4] == "wap" + str(result[i][1]):       # 優先度が2のWAPを使用しているデバイスはないか
                    #     print("mark 3")
                    #     device_name = msg.Args["device_route"][j][5:]
                    #     print("優先度が2のWAPを使用しているデバイス名", device_name)
                    #     k = 0
                    #
                    #     for n in msg.Args["app_name"]:
                    #         if msg.Args["app_name"][k][3:] == result[i][0]:    # 優先度が2のアプリを使用しているデバイス
                    #             pass
                    #         #     優先度が2のWAPが使用しているGWを探す
                    #         # そのGWに接続している他のWAPがあるか
                    #         # あったらunused_routeから他のGWへ接続させる
                    #
                    #         k += 1

                        # k = 0
                        # for n in msg.Args["app_name"]:
                        #     if msg.Args["app_name"][k][0:3] == device_name:
                        #         print(msg.Args["app_name"][k])
                        #     k += 1

                        # if msg.Args["app_name"]
                    # print(msg.Args["device_route"][j][0:4])
                    # print("wap" + str(result[i][1]))
                    # print(type(msg.Args["device_route"][j][0:4]))
                    j += 1
                # print("i=",i)
            i += 1
        msg.Args = msg.Args["route"]
        print("結果",msg.Args)






    # DBで現在時刻で稼働しているアプリ検索
    # なかったらそのままスルー
    # あったら、アプリ名・WAPを取り出す
    # まず、そのアプリが使われていないか
    # HIから指定されたWAPは使われていないか
    # 使われていたらその経路を使用しているデバイス・WAP・GWをC-CONTから送られてきた使用されていない経路へ変更
    # 経路変更が終わったらOperationへ送信


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

