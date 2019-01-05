from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT
from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable
# -*- coding: utf-8 -*-

from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage
import json

class ResourceConnectorAgent(EdgeBaseAgent):
    # pass
    ACTIONS = {
        'OUTPUT': 'act_output'
    }

    def act_output(self, msg: AgentMessage):
        print(">>>", msg.Args)


class APP():
    def __init__(self, name, app1, app2, **kwargs):
        self.name = name
        # self.app1 = kwargs("app1", 0)
        self.app1 = app1
        self.priority1 = kwargs.get("priority1", 0)
        # self.app2 = kwargs("app2", 0)
        self.app2 = app2
        self.priority2 = kwargs.get("priority2", 0)
        # self.event2 = kwargs.get("event2", 0)
        self.situation = []
        self.route = kwargs.get("route", 0)
        print("00000")

    def save1(self):
        print(self.app1, self.situation)
        # # # エージェントの起動
        # agt = ResourceConnectorAgent("INPUT")
        # msg = AgentMessage()
        # msg.Type = "INFORM"
        # msg.From = agt.name
        # msg.To = "OUTPUT"
        # msg.Action = "OUTPUT"
        # # msg.Args = {self.app1}
        # msg.Args = {self.app1:self.situation
        # }
        # agt.send_message(msg, qos=0)
        # # return self.situation
        # # print(type(self.situation))

    def save2(self):
        print(self.app2, self.situation)
        print("111111-2")

    def save3(self):
        # print(self.app2, self.situation)
        print("Same priority")
        print("111111-3")
        # return "aa"




class AdVariables(BaseVariables):
    def __init__(self, app):
        self.app = app

    @string_rule_variable
    def name(self):
        return self.app.name

    @string_rule_variable
    def app1(self):
        return self.app.app1

    @string_rule_variable
    def priority1(self):
        # print("priority1")
        return self.app.priority1

    @string_rule_variable
    def app2(self):
        return self.app.app2

    @string_rule_variable
    def priority2(self):
        # print("priority2")
        return self.app.priority2

    @string_rule_variable
    def event2(self):
        return self.app.event2


class AdActions(BaseActions):
    def __init__(self, app):
        self.app = app
        # print("121212")
        # self.add_situation1()   ##

    def send(self,situation):
        #    エージェントの起動
        agt = ResourceConnectorAgent("ab")
        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = agt.name
        msg.To = "OUTPUT"
        msg.Action = "OUTPUT"
        # msg.Args = {self.app1}
        msg.Args = {"situation":situation
        }
        agt.send_message(msg, qos=0)
        # print(situation)


    @rule_action(params={"situation": FIELD_TEXT})
    def add_situation1(self, situation):
        self.app.situation.append(situation)
        self.app.save1()
        # reslt = self.app.save1()
        # self.state = reslt
        self.send(situation)



    def add_situation2(self, situation):
        self.app.situation.append(situation)
        self.app.save2()

    def add_situation3(self, situation):
        self.app.situation.append(situation)
        self.app.save3()
        # aa = self.app.save3()
        # return aa




# app1 > app2 →　save1
# app1 < app2 →　save2
# app1 = app2 →　save3

def main():

    print("main")
    rules = [{
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'high'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'high'},
            ]
        },
        'actions': [
            {'name': 'add_situation3', 'params': {'situation': 'situation_a'}},
        ],
    },
    {
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'high'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'medium'},
            ]
        },
        'actions': [
            {'name': 'add_situation1', 'params': {'situation': 'situation_b'}},
        ],
    },
    {
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'high'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'low'},
            ]
        },
        'actions': [
            {'name': 'add_situation1', 'params': {'situation': 'situation_c'}},
            # print("333")
        ],
    },
    {
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'medium'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'high'},
            ]
        },
        'actions': [
            {'name': 'add_situation2', 'params': {'situation': 'situation_d'}},
        ],
    },
    {
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'medium'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'medium'},
            ]
        },
        'actions': [
            {'name': 'add_situation3', 'params': {'situation': 'situation_e'}},
        ],
    },
    {
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'medium'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'low'},
            ]
        },
        'actions': [
            {'name': 'add_situation1', 'params': {'situation': 'situation_f'}},
        ],
    },
    {
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'low'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'high'},
            ]
        },
        'actions': [
            {'name': 'add_situation2', 'params': {'situation': 'situation_g'}},
        ],
    },
    {
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'low'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'medium'},
            ]
        },
        'actions': [
            {'name': 'add_situation2', 'params': {'situation': 'situation_h'}},
        ],
    },
    {
        'conditions': {
            'all': [
                {'name': 'priority1', 'operator': 'equal_to', 'value': 'low'},
                {'name': 'priority2', 'operator': 'equal_to', 'value': 'low'},
            ]
        },
        'actions': [
            {'name': 'add_situation3', 'params': {'situation': 'situation_i'}},
        ],
    },
    ]

    # iot_app = [
    #     WCA(name='WCA1', prirority='gw2_a', event2='gw2_b', route=['wap1-wap2-gw1', 'wap3-gw2'])
    # ]
    # app_name1 = input("app name >>")
    # app_name = "aa"
    # pri = input("prirority >>")
    # pri = "high"
    # pri = "aa"
    app_name1 = "aa"
    app_name2 = "bb"
    pri1 = input("pri1>>")
    pri2 = input("pri2>>")
    iot_app = [
        APP(name=app_name1, app1=app_name1, priority1=pri1, app2=app_name2, priority2=pri2)
    ]
    for app in iot_app:
        run_all(rule_list=rules,
                defined_variables=AdVariables(app),
                defined_actions=AdActions(app),
                stop_on_first_trigger=True)

    agt = ResourceConnectorAgent("ab", local = True)
    msg = AgentMessage()
    # msg.Type = "INFORM"
    # msg.From = agt.name
    # msg.To = "OUTPUT"
    # msg.Action = "OUTPUT"
    # # msg.Args = {self.app1}
    # msg.Args = {"situation": situation
    #             }
    # agt.send_message(msg, qos=0)
    print(msg.Args)
    print("-------")

if __name__ == '__main__':
    main()