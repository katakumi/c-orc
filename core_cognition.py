# -*- coding: utf-8 -*-

from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
import json
import redis
import mysql.connector
import time
import numpy as np
import itertools
import pymysql.cursors

#
# conn = mysql.connector.connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     password='takumi',
#     database='mysql',
# )
# cursor = conn.cursor()
# # データベース「test」を選択
# cursor.execute("USE test")
# conn.commit()

conn = pymysql.connect(host='localhost',
                    user='root',
                    db='mysql',
                    password='takumi',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

# データベース「test」を選択
cursor.execute("USE test")
conn.commit()



class ResourceConnectorAgent(EdgeBaseAgent):
    #
    ACTIONS = {
        'OUTPUT': 'act_output'
    }


    def act_output(self, msg: AgentMessage):
        # print(">>>", msg.Args)
        print("===============")
        unixtime = time.time()
        # print(msg.Date)
        # data = {"a": 2, "b": 2}
        # msg.Args["cognition"] = data  # 辞書の追加
        # print(msg.Args)
        msg.To = "Decision"  # 宛先の変更

        # r.set(unixtime, msg.Args["WCA_name"])
        # print(r.get(msg.Args["WCA_name"]))
        # r.set(msg.Args["WCA_name"], unixtime)
        # # print(r.get(msg.Args["WCA_name"]))
        # print(r.keys())



        # r.set(msg.Date, msg.Args)
        # print(r.get(msg.Args))

        # agt.send_message(msg, qos=0)  # メッセージ送信
        # print(msg.From)

        # msg.To = "net_hi"
        # agt.send_message(msg, qos=0)
        #


        data = {
            "WCA_name": msg.Args["WCA_name"],
            "INPUT": msg.Args["INPUT"],
            "OUTPUT": msg.Args["OUTPUT"],
            "state": msg.Args["state"],
            "rote1": msg.Args["rote1"],
            "rote2": msg.Args["rote2"],
            "rote3": msg.Args["rote3"],
            "rote4": msg.Args["rote4"],
            "rote5": msg.Args["rote5"],
            "rote6": msg.Args["rote6"],
            "rote7": msg.Args["rote7"],
            "broken1": msg.Args["broken1"],
            "broken2": msg.Args["broken2"],
            "unixtime": unixtime
        }


        # wcaname = data["WCA_name"]
        # print("data",data)
        # print(wcaname)
        # # 2回目以降の書き込みか検索
        # # aaa = "wca2"
        # # sql = "SELECT WCA FROM wca_table WHERE WCA LIKE '%s'" % (aaa,)
        # sql = "SELECT WCA FROM wca_table WHERE WCA LIKE '%s'" % (wcaname,)
        # cursor.execute(sql)
        # bbbb = cursor.fetchall()
        # conn.commit()
        # print(bbbb)

        # if bbbb == "[]":        #データが空の時
        #     print("aaa")
        # # msg.Argsに入っているWCAの情報をそのまま書き込み
        # else:
        #     # 上書き
        #     print("bbb")        #2回目以降(上書き)の処理



        # insertの型の生成
        insert_wca = "INSERT INTO wca_table (WCA, INPUT, OUTPUT, state, rote_1, rote_2, rote_3, rote_4, rote_5, rote_6, " \
                     "rote_7, broken_1, broken_2, UNIXTIME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        # 受け取ったデータの書き込み
        val = (data["WCA_name"], data["INPUT"], data["OUTPUT"], data["state"], data["rote1"], data["rote2"], data["rote3"], \
               data["rote4"], data["rote5"], data["rote6"], data["rote7"], data["broken1"], data["broken2"], data["unixtime"])
        cursor.execute(insert_wca, val)
        conn.commit()


        print("==================================")
        val = "SELECT * FROM wca_table WHERE (WCA, UNIXTIME) IN (SELECT WCA, MAX(UNIXTIME) FROM wca_table GROUP BY WCA );"
        cursor.execute(val)
        result = cursor.fetchall()
        # print("result",result)
        # print(type(result))
        # n = 0
        # for r in result:
        #     print(r)
        #     data[n] = r
        #     print(data[n])
        #     n += 0
        #     print(type(data[n]))
        # #
        # # for i in :
        # #     print(data[i])
        print(result)
        # data = []
        n = 0
        for r in result:
            data[n] = r
            n += 1

        # print("---------------------")

        for k in range(n):
            print(data[k])

        # k = 0
        # for j in result:
        #     # print("--------", data[k])
        #     print(data[k])
        #     k += 1
        #
        # if k > 1 :
        #     print(data[2])
        # if n > 1:
        #     print("=======", data[1]["WCA"])
        #
        # print(len(data))


        # print(aaaa[0])



        # if len(result) > 1:
        #     n = 0
        #     for i in result:
        #         print(data[i])


        # i = 0
        # for j in range(len(result)):
        #     print("----", data[i])
        #     # i += 1
        # # print(type(data[0]))
        # # print(data[0])





        # # 各WCAの最新のデータのみ抽出
        # val = "SELECT * FROM wca_table WHERE (WCA, UNIXTIME) IN (SELECT WCA, MAX(UNIXTIME) FROM wca_table GROUP BY WCA );"
        # cursor.execute(val)
        # aaa = cursor.fetchall()
        # conn.commit()
        # print(aaa)
        # print(type(aaa))
        # # print(len(aaa))
        # # n = len(aaa)
        # # n = 0
        # # dataaa = ()
        # # for i in range(len(aaa)):
        # #     print(i)
        # #     dataaa(n) = aaa[i]
        # info = ["WCA_name", "INPUT", "OUTPUT", "state", "rote1", "rote2", "rote3", "rote4", "rote5", "rote6", "rote7", "broken1", "broken2", "UNIXTIME"]
        # bbb = list(itertools.chain(*aaa))
        # print(bbb)
        # data = dict(zip(info, bbb))
        # print(data)






        # [('1', 10, 10, 20, 20, 20, 30, 41, 42, 52, 53, 0, 0, 1545721358), ('2', 10, 10, 20, 20, 20, 30, 41, 42, 52, 53, 0, 0, 1545721363)]を
        # ('1', 10, 10, 20, 20, 20, 30, 41, 42, 52, 53, 0, 0, 1545721358)と ('2', 10, 10, 20, 20, 20, 30, 41, 42, 52, 53, 0, 0, 1545721363)に変換して
        #
        # n = 0
        # for i in range(len(aaa)):
        #     print("----------")
        #     bbb = list(itertools.chain(*aaa[n]))
        #     data[n] = dict(zip(info, bbb))
        #     print(data[n])
        #     n += 1
        #     # print(type(i))








if __name__ == "__main__":
    print("===============================================================")
    print("OUTPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : Ctrl-c")
    # エージェントの起動
    agt = ResourceConnectorAgent("Cognition", local=True)
    # テーブル「wca_table」の消去
    sql = "DROP TABLE  IF EXISTS wca_table"
    cursor.execute(sql)
    # # Redis に接続
    # r = redis.Redis(host='localhost', port=6379, db=0)
    # # redisのリセット
    # r.flushall()



    # WCA VARCHAR(10),
    # テーブル「wca_table」を作成
    cursor.execute("""CREATE TABLE IF NOT EXISTS wca_table(
                    WCA VARCHAR(10) NOT NULL,
                    INPUT INT default 0,
                    OUTPUT INT default 0,
                    state INT default 0,
                    rote_1 INT default 0,
                    rote_2 INT default 0,
                    rote_3 INT default 0,
                    rote_4 INT default 0,
                    rote_5 INT default 0,
                    rote_6 INT default 0,
                    rote_7 INT default 0,
                    broken_1 INT default 0,
                    broken_2 INT default 0,
                    UNIXTIME INT(15)
                    );""")
    conn.commit()


    # defaultデータ
    # insert_wca = "INSERT INTO wca_table (WCA, INPUT, OUTPUT, state, rote_1, rote_2, rote_3, rote_4, rote_5, rote_6, rote_7, broken_1, broken_2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    # WCA_name = 'wca1'
    # INPUT = 999
    # OUTPUT = 999
    # state = 99
    # rote1 = 99
    # rote2 = 99
    # rote3 = 99
    # rote4 = 99
    # rote5 = 99
    # rote6 = 99
    # rote7 = 99
    # broken1 = 9
    # broken2 = 9
    # val = (WCA_name, INPUT, OUTPUT, state, rote1, rote2, rote3, rote4, rote5, rote6, rote7, broken1, broken2)
    # cursor.execute(insert_wca, val)
    # conn.commit()
    # WCA_name = 'wca2'
    # INPUT = 999
    # OUTPUT = 999
    # state = 99
    # rote1 = 99
    # rote2 = 99
    # rote3 = 99
    # rote4 = 99
    # rote5 = 99
    # rote6 = 99
    # rote7 = 99
    # broken1 = 9
    # broken2 = 9
    # val = (WCA_name, INPUT, OUTPUT, state, rote1, rote2, rote3, rote4, rote5, rote6, rote7, broken1, broken2)
    # cursor.execute(insert_wca, val)
    # conn.commit()
    # WCA_name = 'wca3'
    # INPUT = 999
    # OUTPUT = 999
    # state = 99
    # rote1 = 99
    # rote2 = 99
    # rote3 = 99
    # rote4 = 99
    # rote5 = 99
    # rote6 = 99
    # rote7 = 99
    # broken1 = 9
    # broken2 = 9
    # val = (WCA_name, INPUT, OUTPUT, state, rote1, rote2, rote3, rote4, rote5, rote6, rote7, broken1, broken2)
    # cursor.execute(insert_wca, val)
    # conn.commit()

