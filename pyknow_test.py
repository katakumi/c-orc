from pyknow import *
# class Light(Fact):
#     # """Info about the traffic light."""
#     pass


class RouteControl(KnowledgeEngine):
    @Rule(Fact(rote="gw1-wap1"),(Fact(situation="ap1")))
    def pattern1(self):
        # print("aaa")
        self.state = "situation_a"

    @Rule(Fact(rote="gw2-wap2"),(Fact(situation="ap2")))
    def pattern2(self):
        # print("bbb")
        self.state = "situation_b"

    @Rule(Fact(rote="a"), (Fact(situation="a")))
    def pattern3(self):
        # self.pri = 1
        # print(self.pri)
        self.state = 1


engine = RouteControl()
engine.reset()
# engine.declare(Fact(Light(data=str(input()))))
engine.declare(
    Fact(rote=str(input("rote>>>"))),
    Fact(situation=str(input("situation>>>"))),
    # Fact(AppPriority=int(input("AppPriority>>>")))
)
engine.run()
# print(engine.state)
pri = engine.state
print(pri)
