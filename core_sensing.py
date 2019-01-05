from flask import Flask, render_template, request
import json
from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
app = Flask(__name__)


class ResourceConnectorAgent(EdgeBaseAgent):
    #
    ACTIONS = {
        'OUTPUT': 'act_output'
    }



    def act_output(self, msg: AgentMessage):
        def act_count(name1, name2):
            i = 0
            count = 0
            for n in msg.Args[name1]:
                if msg.Args[name1][i].count(name2):
                    count += 1
                i += 1
            return count

        print(">>>", msg.Args)

        # i = 0
        # count = 0
        # for n in msg.Args["rote"]:
        #     if msg.Args["rote"][i].count("gw1"):
        #         count += 1
        #     i += 1
        # print(count)

        gw1 = act_count("rote", "gw1")
        gw2 = act_count("rote", "gw2")
        wap1 = act_count("rote", "wap1")
        wap2 = act_count("rote", "wap2")
        wap3 = act_count("rote", "wap3")

        print("gw1 connection=", gw1)
        print("gw2 connection=", gw2)
        print("wap1 connection=", wap1)
        print("wap2 connection=", wap2)
        print("wap3 connection=", wap3)
        data = {
            "gw":{"gw1": gw1,
                  "gw2": gw2
                  },
            "wap":{"wap1": wap1,
                   "wap2": wap2,
                   "wap3": wap3
                   }
        }




        # print(msg.Date)
        # data = {"a": 1, "b": 1}
        # msg.Args["sensing"] = data  # 辞書の追加
        # print(msg.Args)
        # print(type(msg.Args))

        # # 全部のWCAのデータが送られてきて、ばらばらに送られてきたデータをまとめて送信する処理
        # msg.Args = {"wca1": "state", "rote11": "ab", "rote12": "bc", "broken11": "a",
        #             "wca2": "state", "rote21": "ab", "rote22": "bc", "broken21": "c"
        #             }

        msg.Args = data
        # msg.To = "Cognition"            #宛先の変更
        msg.To = "Cognition"
        agt.send_message(msg, qos=0)    #メッセージ送信



    # ACTIONS = {
    #     'OUTPUT': 'act_output'
    # }
    #
    # msg.Action = "OUTPUT"
    #



if __name__ == "__main__":
    print("===============================================================")
    print("OUTPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : Ctrl-c")
    # エージェントの起動
    agt = ResourceConnectorAgent("Sensing", local=True)


