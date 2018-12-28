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

        print(">>>", msg.Args)
        print(msg.Date)
        # data = {"a": 1, "b": 1}
        # msg.Args["sensing"] = data  # 辞書の追加
        # print(msg.Args)
        # print(type(msg.Args))

        # # 全部のWCAのデータが送られてきて、ばらばらに送られてきたデータをまとめて送信する処理
        # msg.Args = {"wca1": "state", "rote11": "ab", "rote12": "bc", "broken11": "a",
        #             "wca2": "state", "rote21": "ab", "rote22": "bc", "broken21": "c"
        #             }

        msg.To = "Cognition"            #宛先の変更
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


