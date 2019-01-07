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

conn = pymysql.connect(host='localhost',
                       user='root',
                       db='test',
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
        print(">>>", msg.Args)
        # wapの数が分かっていなくても個数を検出できる処理
        # aa = [l for l in msg.Args["route"] if 'wap' in l]
        # print(aa)
        def act_count(name):    # GW、WAPの接続数カウント
            i = 0
            count = 0
            for n in msg.Args["route"]:
                if msg.Args["route"][i].count(name):
                    count += 1
                i += 1
            return count

        gw1 = act_count("gw1")
        gw2 = act_count("gw2")
        wap1 = act_count("wap1")
        wap2 = act_count("wap2")
        wap3 = act_count("wap3")

        print("gw1 connection=", gw1)
        print("gw2 connection=", gw2)
        print("wap1 connection=", wap1)
        print("wap2 connection=", wap2)
        print("wap3 connection=", wap3)
        waps = {"wap1": wap1,
                "wap2": wap2,
                "wap3": wap3
                }

        # 偏りの検出
        device_sum = wap1 + wap2 + wap3
        print("device sum", device_sum)
        wap_sum = 3
        ave = device_sum / wap_sum      # wap1台当たりの平均接続デバイス数
        print("average", ave)
        i = 0
        if ave > 1:
            for n in waps:
                name1 = i + 1
                name2 = "wap"+ str(name1)
                if ave < waps[name2]:    # 平均台数以上繋がっているWAPを表示
                    biased = name2
                i += 1
        else:
                biased = "none"
        # unixtime = time.time()
        # print(msg.Date)
        # data = {"a": 2, "b": 2}
        # msg.Args["cognition"] = data  # 辞書の追加
        # print(msg.Args)

        # # wapに接続されているデバイスの合計
        # i = 0
        # sum = 0
        # leng = 0
        # # for n in msg.Args["wap"]:
        # for n in msg.Args["route"]:
        #     name1 = i + 1
        #     name2 = "wap"+ str(name1)
        #     # print(name2)
        #     sum += msg.Args["wap"][name2]
        #     i += 1
        #     leng += 1
        # print("device total", sum)
        # # sum = wap1 + wap2 + wap3
        # # デバイス数÷WAP数
        # ave = sum / leng
        # print("agerage", ave)
        #
        # # 平均と比較してWAPに接続されているデバイス数の偏りがないか
        # i = 0
        # biased = "none"
        # if ave > 1:
        #     print("----")
        #     for n in msg.Args["wap"]:
        #         name1 = i + 1
        #         name2 = "wap" + str(name1)
        #         if ave < msg.Args["wap"][name2]:
        #             biased = name2
        #         i += 1
        # print("biased", biased)

        # DBにsituationを保存
        # Decisionに送信
        # Cognitionの処理は終わり
        # ここからDecision
        # DBからsituationを取り出す or Cognitionから送信してもらう
        # 優先するアプリとそのWAPをDBから検索
        # WAPが使われていたら経路変更

        # ave = sum / count
        # print(ave)

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
        situation = {           # Decisionへ送信するsituation
            "gw": {"gw1": gw1,
                   "gw2": gw2
                   },
            # "wap": {"wap1": wap1,
            #         "wap2": wap2,
            #         "wap3": wap3
            #         },
            "wap": waps,
            "biased": biased
        }
        msg.Args["situation"] = situation
        print(msg.Args)
        msg.To = "Decision"  # 宛先の変更
        msg.Action = "OUTPUT_cognition"
        agt.send_message(msg, qos=0)
        #

        # data = {
        #     "WCA_name": msg.Args["WCA_name"],
        #     "INPUT": msg.Args["INPUT"],
        #     "OUTPUT": msg.Args["OUTPUT"],
        #     "state": msg.Args["state"],
        #     "rote1": msg.Args["rote1"],
        #     "rote2": msg.Args["rote2"],
        #     "rote3": msg.Args["rote3"],
        #     "rote4": msg.Args["rote4"],
        #     "rote5": msg.Args["rote5"],
        #     "rote6": msg.Args["rote6"],
        #     "rote7": msg.Args["rote7"],
        #     "broken1": msg.Args["broken1"],
        #     "broken2": msg.Args["broken2"],
        #     "unixtime": unixtime
        # }

        # # insertの型の生成
        # insert_wca = "INSERT INTO wca_table (WCA, INPUT, OUTPUT, state, rote_1, rote_2, rote_3, rote_4, rote_5, rote_6, " \
        #              "rote_7, broken_1, broken_2, UNIXTIME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        # # 受け取ったデータの書き込み
        # val = (data["WCA_name"], data["INPUT"], data["OUTPUT"], data["state"], data["rote1"], data["rote2"], data["rote3"], \
        #        data["rote4"], data["rote5"], data["rote6"], data["rote7"], data["broken1"], data["broken2"], data["unixtime"])
        # cursor.execute(insert_wca, val)
        # conn.commit()
        #
        #
        # print("==================================")
        # val = "SELECT * FROM wca_table WHERE (WCA, UNIXTIME) IN (SELECT WCA, MAX(UNIXTIME) FROM wca_table GROUP BY WCA );"
        # cursor.execute(val)
        # result = cursor.fetchall()
        #
        # print(result)
        # # data = []
        # n = 0
        # for r in result:
        #     data[n] = r
        #     n += 1
        #
        # # print("---------------------")
        #
        # for k in range(n):
        #     print(data[k])


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
