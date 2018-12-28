# -*- coding: utf-8 -*-

from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
import json
import redis


class ResourceConnectorAgent(EdgeBaseAgent):
    #
    ACTIONS = {
        'OUTPUT': 'act_output'
    }

    def act_output(self, msg: AgentMessage):
        print(">>>", msg.Args)
        print(msg.Date)
        data = {"a": 4, "b": 4}
        msg.Args["operation"] = data  # 辞書の追加
        print(msg.Args)
        # msg.To = "operation"  # 宛先の変更
        # agt.send_message(msg, qos=0)  # メッセージ送信


if __name__ == "__main__":
    print("===============================================================")
    print("OUTPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : Ctrl-c")
    # エージェントの起動
    agt = ResourceConnectorAgent("Operation", local=True)


