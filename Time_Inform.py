# -*- coding: utf-8 -*-

from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
import json
import time

class ResourceConnectorAgent(EdgeBaseAgent):
    pass


if __name__ == "__main__":
    # エージェントの起動
    agt = ResourceConnectorAgent("INPUT")

    print("===============================================================")
    print("INPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : q [Enter]")


    def worker():
        print(time.time())
        time.sleep(2)


    interval = 0
    while True:
        worker()
        time.sleep(interval)



        # SAMへ送信
        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = agt.name
        msg.To = "Decision"
        msg.Action = "TIME"
        # msg.Args = {"SENTENCE"}
        # msg.TaskID = {"SENTENCE"}

        agt.send_message(msg, qos=0)
        print("A message was sent.")
