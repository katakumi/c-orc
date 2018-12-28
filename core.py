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
        print(">>>", msg.Args['SENTENCE'], msg.Date)
        # print("Task Name  : ", msg.TaskName)
        # print("WCAs       : ", msg.WCAs)
        # print("Start Date : ", msg.StartDate)
        # print("Start Time : ", msg.StartTime)
        # print("End Date   : ", msg.EndDate)
        # print("End Time   : ", msg.EndTime)
        #print(msg.Args)


    #
    # # Redis に接続します
    # r = redis.Redis(host='localhost', port=6379, db=0)
    #
    # # 'hoge' というキーで 'moge' という値を追加します
    # r.set('hoge','moge')
    #
    # # 追加した値を取得して表示します
    # hoge = r.get('hoge')
    # print(hoge.decode())
    #
    # # 追加した値を削除します
    # result = r.delete('hoge')

    r = redis.Redis(host='localhost', port=6379, db=0)





if __name__ == "__main__":
    print("===============================================================")
    print("OUTPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : Ctrl-c")
    # エージェントの起動
    agt = ResourceConnectorAgent("OUTPUT", local=True)


