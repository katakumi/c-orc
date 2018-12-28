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

       # print("broken ", msg.Args["broken"])



        msg.To = "Decision"            #宛先の変更
        agt.send_message(msg, qos=0)    #メッセージ送信


if __name__ == "__main__":
    print("===============================================================")
    print("OUTPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : Ctrl-c")
    # エージェントの起動
    agt = ResourceConnectorAgent("net_hi", local=True)


