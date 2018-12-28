# -*- coding: utf-8 -*-

from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
import json


class LogicAgent(EdgeBaseAgent):
    #
    ACTIONS = {
        'CC_Inform_State': 'CC_inform_state',
        'CO_Inform_Request': 'CO_inform_request'
    }

    def CC_inform_state(self, msg: AgentMessage):
        print('CC-inform_state start')

    def CO_inform_request(self, msg: AgentMessage):
        print('CO-inform-request start')


if __name__ == "__main__":
    print("===============================================================")
    print("Cognitive Orchestrator core")
    print("===============================================================")
    # エージェントの起動
    agt = LogicAgent("C-ORC-core", local=True)


