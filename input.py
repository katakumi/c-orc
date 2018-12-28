# -*- coding: utf-8 -*-

from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
import json

class ResourceConnectorAgent(EdgeBaseAgent):
    pass


if __name__ == "__main__":
    # エージェントの起動
    agt = ResourceConnectorAgent("INPUT")

    print("===============================================================")
    print("INPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : q [Enter]")

    while True:
        text = input(">>>")

        if text == 'q':
            break

        data = {'Task Name':'taskname',
        'WCAs ':'wcas'} #,
        # 'Start Date ':startdate,
        # 'Start Time ':starttime,
        # 'End Date ':enddate,
        # 'End Time ':endtime}

        # SAMへ送信
        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = agt.name
        msg.To = "OUTPUT"
        msg.Action = "OUTPUT"
        msg.Args = {"SENTENCE" : text}
        msg.TaskID = {"SENTENCE" : data }        ###

        agt.send_message(msg, qos=0)
        print("A message was sent.")

        #time.sleep(0.1)
