from flask import Flask, render_template, request
import json
from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
app = Flask(__name__)


class ResourceConnectorAgent(EdgeBaseAgent):
    pass

if __name__ == "__main__":
    # エージェントの起動
    agt = ResourceConnectorAgent("INPUT")

    while True:
        send = input(">>>")
        # WCA_name = input(" WCA_name> ")
        # INPUT = input(" INPUT > ")
        # OUTPUT = input(" OUTPUT > ")
        # state = input(" state > ")
        # rote1 = input(" rote1 > ")

        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = agt.name
        # msg.To = "Cognition"  # 宛先の変更
        msg.To = "Sensing"
        msg.Action = "OUTPUT"
        msg.Args = {
            # "rote": ("gw1-wap1-d1","gw1-wap1-d1","gw2-wap2-d2"),
            # "route": ("gw1-wap1-d1", "gw1-wap1-d2", "gw1-wap1-d1", "gw2-wap2-d2"),
            # "unused_rote": ("gw1-wap2", "gw2-wap3"),
            # "use_app": ("d1-app1","d2-app2","d3-app3")
            "route":("gw1-wap1-d1","gw2-wap2-d2","gw2-wap3-d3"),
            # "device_route":("wap1-d1","wap2-d2","wap3-d3"),
            "app_name":("d1-aa","d2-aa","d3-bb"),
            # "unused_route":("gw1-wap2","gw2-wap1","gw2-wap3")
            # "unused_route":("gw1-wap2","gw2-wap1")
            "unused_route": ("gw2-wap1",)
        }

        # msg.Args = {
        #     "WCA_name": WCA_name,
        #     # "INPUT": INPUT,
        #     # "OUTPUT": OUTPUT,
        #     # "state": state,
        #     # "rote1": rote1,
        #     "INPUT": 10,
        #     "OUTPUT": 10,
        #     "state": 20,
        #     "rote1": 20,
        #     "rote2": 20,
        #     "rote3": 30,
        #     "rote4": 41,
        #     "rote5": 42,
        #     "rote6": 52,
        #     "rote7": 53,
        #     "broken1": 0,
        #     "broken2": 0,
        # }
        print(">>>", msg.Args)
        agt.send_message(msg, qos=0)    #メッセージ送信

