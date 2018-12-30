from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT
from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable


class data():
    # def __init__(self, name, **kwargs):
    #     self.name = name
    #     self.event1 = kwargs.get("event1", 0)
    #     self.event2 = kwargs.get("event2", 0)
    #     self.situation = []
    #     self.route = kwargs.get("route", 0)
    #
    # def save(self):
    #     print(self.name, self.situation)
    def __init__(self, app1, app2, priority1, priority2, type1, type2):    #**kwargs
        self.app1 = app1
        self.app2 = app2
        self.priority1 = priority1
        self.priority2 = priority2
        self.type1 = type1
        self.type2 = type2
        # self.priority1 = kwargs.get("priority1", 0)
        # self.priority2 = kwargs.get("priority2", 0)
        # self.type1 = kwargs.get("type1", 0)
        # self.type2 = kwargs.get("type2", 0)
        self.situation = []
        # self.route = kwargs.get("route", 0)

    def save(self):
        print(self.data, self.situation)


class AdVariables(BaseVariables):
    # def __init__(self, wca):
    #     self.wca = wca
    #
    # @string_rule_variable
    # def name(self):
    #     return self.wca.name
    #
    # @string_rule_variable
    # def event1(self):
    #     return self.wca.event1
    #
    # @string_rule_variable
    # def event2(self):
    #     return self.wca.event2
    def __init__(self, data):
        self.data = data

    @string_rule_variable
    def app1(self):
        return self.data.app1

    @string_rule_variable
    def app2(self):
        return self.data.app2

    @string_rule_variable
    def priority1(self):
        return self.data.priority1

    @string_rule_variable
    def priority2(self):
        return self.data.priority2

    @string_rule_variable
    def type1(self):
        return self.data.type1

    @string_rule_variable
    def type2(self):
        return self.data.type2


class AdActions(BaseActions):
    def __init__(self, data):
        self.data = data
    #
    # @rule_action(params={"situation": FIELD_TEXT})
    # def add_situation(self, situation):
    #     self.data.situation.append(situation)
    #     self.data.save()


def main():
    rules = [{
        'conditions': {
            'all': [
                {'app1': 'priority1', 'operator': 'equal_to', 'value': '0'},
                {'app1': 'type1', 'operator': 'equal_to', 'value': '0'},
                {'app2': 'priority2', 'operator': 'equal_to', 'value': '0'},
                {'app2': 'type2', 'operator': 'equal_to', 'value': '0'},
            ]
        },
        'actions': [
            # {'name': 'add_situation', 'params': {'situation': 'situation_a'}},
            print("Same priority and type")
        ],
    },
        # {
        #     'conditions': {
        #         'all': [
        #             {'app1': 'priority1', 'operator': 'equal_to', 'value': '0'},
        #             {'app1': 'type1', 'operator': 'equal_to', 'value': '0'},
        #             {'app2': 'priority2', 'operator': 'equal_to', 'value': '0'},
        #             {'app2': 'type2', 'operator': 'equal_to', 'value': '0'},
        #         ]
        #     },
        #     'actions': [
        #         # {'name': 'add_situation', 'params': {'situation': 'situation_a'}},
        #         print("Same priority and type")
        #     ],
        # },
    ]

    # rules = [{
    #     'conditions': {
    #         'all': [
    #             {'name': 'event1', 'operator': 'equal_to', 'value': 'gw2_a'},
    #             {'name': 'event2', 'operator': 'equal_to', 'value': 'gw2_b'},
    #         ]
    #     },
    #     'actions': [
    #         {'name': 'add_situation', 'params': {'situation': 'situation_a'}},
    #     ],
    # },
    #     {
    #         'conditions': {
    #             'all': [
    #                 {'name': 'event1', 'operator': 'equal_to', 'value': 'a'},
    #                 {'name': 'event2', 'operator': 'equal_to', 'value': 'a'},
    #             ]
    #         },
    #         'actions': [
    #             {'name': 'add_situation', 'params': {'situation': 'situation_aa'}},
    #         ],
    #     }
    # ]

    # wcas = [
    #     WCA(name='WCA1', event1='gw2_a', event2='gw2_b', route=['wap1-wap2-gw1', 'wap3-gw2'])
    # ]
    # wcas = [
    #     WCA(name=WCA1, event1=event1, event2=event2, route=['wap1-wap2-gw1', 'wap3-gw2'])
    # ]

    # for wca in wcas:
    #     run_all(rule_list=rules,
    #             defined_variables=AdVariables(wca),
    #             defined_actions=AdActions(wca),
    #             stop_on_first_trigger=True)
    app1 = "aaa"
    priority1 = 2
    type1 = 2
    app2 = "bbb"
    priority2 = 2
    type2 = 2
    wcas = [
        data(app1, priority1, type1, app2, priority2, type2)
    ]
    # wcas = [
    #     WCA(name='WCA1', event1='gw2_a', event2='gw2_b', route=['wap1-wap2-gw1', 'wap3-gw2'])
    # ]
    for wca in wcas:
        run_all(rule_list=rules,
            defined_variables=AdVariables(wca),
            defined_actions=AdActions(wca),
            stop_on_first_trigger=True)


if __name__ == '__main__':
    # WCA1 = input("name >>")
    # event1 = input("event1 >>")
    # event2 = input("event2 >>")
    # main(WCA1, event1, event2)
    # app1 = "aaa"
    # priority1 = 2
    # type1 = 2
    # app2 = "bbb"
    # priority2 = 2
    # type2 = 2
    # main(app1,priority1,type1,app2,priority2,type2)
    main()
