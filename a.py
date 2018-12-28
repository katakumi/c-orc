from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT
from business_rules.variables import BaseVariables, numeric_rule_variable, string_rule_variable


class WCA():
    def __init__(self, name, **kwargs):
        self.name = name
        self.event1 = kwargs.get("event1", 0)
        self.event2 = kwargs.get("event2", 0)
        self.situation = []
        self.route = kwargs.get("route", 0)

    def save(self):
        print(self.name, self.situation)


class AdVariables(BaseVariables):
    def __init__(self, wca):
        self.wca = wca

    @string_rule_variable
    def name(self):
        return self.wca.name

    @string_rule_variable
    def event1(self):
        return self.wca.event1

    @string_rule_variable
    def event2(self):
        return self.wca.event2


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
                {'name': 'event1', 'operator': 'equal_to', 'value': 'gw2_a'},
                {'name': 'event2', 'operator': 'equal_to', 'value': 'gw2_b'},
            ]
        },
        'actions': [
            {'name': 'add_situation', 'params': {'situation': 'situation_a'}},
        ],
    }]

    wcas = [
        WCA(name='WCA1', event1='gw2_a', event2='gw2_b', route=['wap1-wap2-gw1', 'wap3-gw2'])
    ]
    for wca in wcas:
        run_all(rule_list=rules,
                defined_variables=AdVariables(wca),
                defined_actions=AdActions(wca),
                stop_on_first_trigger=True)

    rules = [{
        'conditions': {
            'all': [
                {'name': 'event1', 'operator': 'equal_to', 'value': 'gw2_a'},
                {'name': 'event2', 'operator': 'equal_to', 'value': 'gw2_b'},
            ]
        },
        'actions': [
            {'name': 'add_situation', 'params': {'situation': 'situation_b'}},
        ],
    }]

    for wca in wcas:
        run_all(rule_list=rules,
                defined_variables=AdVariables(wca),
                defined_actions=AdActions(wca),
                stop_on_first_trigger=True)


if __name__ == '__main__':
    main()