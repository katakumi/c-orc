from pyknow import *
# class Light(Fact):
#     # """Info about the traffic light."""
#     pass


class RouteControl(KnowledgeEngine):
    # @Rule(Fact(rote="gw1-wap1"),(Fact(situation="ap1")))
    # def pattern1(self):
    #     # print("aaa")
    #     self.state = "situation_a"
    #
    # @Rule(Fact(rote="gw2-wap2"),(Fact(situation="ap2")))
    # def pattern2(self):
    #     # print("bbb")
    #     self.state = "situation_b"

    @Rule(Fact(priority1=1), (Fact(priority2=1)))
    def pattern3(self):
        # self.pri = 1
        # print(self.pri)
        self.state = 1

    # @Rule(Fact(priority1=MATCH.priority1 & GE(Fact(priority2=MATCH.priority2))))
    # @Rule(Fact(priority1=MATCH.priority1) & GE(2))#(Fact(priority2=MATCH.priority2)))
    @Rule(Fact(priority1=Fact(priority2=MATCH.priority2)))
    def pattern3(self):
        self.state = 2


engine = RouteControl()
engine.reset()
# engine.declare(Fact(Light(data=str(input()))))
engine.declare(
    Fact(priority1=int(input("priority1>>>"))),
    Fact(priority2=int(input("priority2>>>"))),
    # Fact(AppPriority=int(input("AppPriority>>>")))
)
engine.run()
# print(engine.state)
pri = engine.state
print(pri)
