from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT
from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable


class WCA():
    def __init__(self, name, **kwargs):
        self.name = name
        self.name1 = kwargs.get("name1", 0)
        self.name2 = kwargs.get("name2", 0)
        self.prirority1 = kwargs.get("prirority1", 0)
        self.type1 = kwargs.get("type1", 0)
        self.prirority2 = kwargs.get("prirority2", 0)
        self.type2 = kwargs.get("type2", 0)
        self.situation = []
        self.route = kwargs.get("route", 0)

    def save(self):
        print(self.name, self.situation)


class AdVariables(BaseVariables):
    def __init__(self, wca):
        self.wca = wca

    @string_rule_variable
    def name1(self):
        return self.wca.name1

    @string_rule_variable
    def name2(self):
        return self.wca.name2

    @string_rule_variable
    def prirority1(self):
        return self.wca.prirority1

    @string_rule_variable
    def type1(self):
        return self.wca.type1

    @string_rule_variable
    def prirority2(self):
        return self.wca.prirority2

    @string_rule_variable
    def type2(self):
        return self.wca.type2


class AdActions(BaseActions):
    def __init__(self, wca):
        self.wca = wca

    @rule_action(params={"situation": FIELD_TEXT})
    def add_situation(self, situation):
        self.wca.situation.append(situation)
        self.wca.save()


def main():
    rules = [{
        'conditions': {
            'all': [
                {'name1': 'prirority1', 'operator': 'equal_to', 'value': 'a'},
                {'name1': 'type1', 'operator': 'equal_to', 'value': 'a'},
                {'name1': 'prirority2', 'operator': 'equal_to', 'value': 'a'},
                {'name1': 'type2', 'operator': 'equal_to', 'value': 'a'},

            ]
        },
        'actions': [
            {'name1': 'add_situation', 'params': {'situation': 'situation_a'}},
        ],
    },
    # {
    #     'conditions': {
    #         'all': [
    #             {'name': 'type1', 'operator': 'equal_to', 'value': 'gw2_a'},
    #             {'name': 'type2', 'operator': 'equal_to', 'value': 'gw2_b'},
    #         ]
    #     },
    #     'actions': [
    #         {'name': 'add_situation', 'params': {'situation': 'situation_aa'}},
    #     ],
    # }
    ]

    # wcas = [
    #     WCA(name='WCA1', prirority1='gw2_a', prirority2='gw2_b', route=['wap1-wap2-gw1', 'wap3-gw2'])
    # ]
    appname1 = input("app1 name >>>")
    pri1 = input("prirority1 >>>")
    ty1 = input("type1 >>>")
    pri2 = input("prirority2 >>>")
    ty2 = input("type2 >>>")
    wcas = [
        WCA(name=appname1, name1=appname1, prirority1=pri1, type1=ty1, prirority2=pri2, type2=ty2)
    ]

    for wca in wcas:
        run_all(rule_list=rules,
                defined_variables=AdVariables(wca),
                defined_actions=AdActions(wca),
                stop_on_first_trigger=True)

    # rules = [{
    #     'conditions': {
    #         'all': [
    #             {'name': 'prirority1', 'operator': 'equal_to', 'value': 'gw2_a'},
    #             {'name': 'prirority2', 'operator': 'equal_to', 'value': 'gw2_b'},
    #         ]
    #     },
    #     'actions': [
    #         {'name': 'add_situation', 'params': {'situation': 'situation_b'}},
    #     ],
    # }]
    #
    # for wca in wcas:
    #     run_all(rule_list=rules,
    #             defined_variables=AdVariables(wca),
    #             defined_actions=AdActions(wca),
    #             stop_on_first_trigger=True)


if __name__ == '__main__':
    main()