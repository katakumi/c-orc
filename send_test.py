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
        WCA_name = input(" WCA_name> ")
        # INPUT = input(" INPUT > ")
        # OUTPUT = input(" OUTPUT > ")
        # state = input(" state > ")
        # rote1 = input(" rote1 > ")

        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = agt.name
        # msg.To = "Cognition"  # 宛先の変更
        msg.To = "Cognition"
        msg.Action = "OUTPUT"

        msg.Args = {
            "WCA_name": WCA_name,
            # "INPUT": INPUT,
            # "OUTPUT": OUTPUT,
            # "state": state,
            # "rote1": rote1,
            "INPUT": 10,
            "OUTPUT": 10,
            "state": 20,
            "rote1": 20,
            "rote2": 20,
            "rote3": 30,
            "rote4": 41,
            "rote5": 42,
            "rote6": 52,
            "rote7": 53,
            "broken1": 0,
            "broken2": 0,
        }
        print(">>>", msg.Args)
        agt.send_message(msg, qos=0)    #メッセージ送信

