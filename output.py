
from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
import json

class ResourceConnectorAgent(EdgeBaseAgent):
    #
    ACTIONS = {
        'OUTPUT' :     'act_output'
    }

    def act_output(self, msg:AgentMessage):
        print(">>>", msg.Args['SENTENCE'], msg.Date)
        #print(">>>", msg.TaskID['SENTENCE'], msg.Date)


if __name__ == "__main__":
    print("===============================================================")
    print("OUTPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : Ctrl-c")
    # エージェントの起動
    agt = ResourceConnectorAgent("OUTPUT", local = True)
