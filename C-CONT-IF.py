from flask import Flask, render_template, request
import json
from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage

app = Flask(__name__)


class ResourceConnectorAgent(EdgeBaseAgent):
    #
    ACTIONS = {
        'OUTPUT': 'act_output'
    }

    def act_output(self, msg: AgentMessage):
        print(">>>", msg.Args)
        print(msg.Date)
        # data = {"a": 1, "b": 1}
        # msg.Args["sensing"] = data  # 辞書の追加
        # c_contA = {"c_cont1":{
        #     "State": "0",
        #     "rote":
        #         {"rote1": {"wap11", "wap12"},
        #          "rote2": {"wap12", "wap13"},
        #          "rote3": {"wap13", "wap14"},
        #          },
        #     "broken": {"wap11", "wap12"},
        # }}
        # c_contB = {"c_cont2": {
        #     'State': '0',
        #     'rote':
        #         {'rote1': {'wap21', 'wap22'},
        #          'rote2': {'wap22', 'wap23'},
        #          'rote3': {'wap23', 'wap24'},
        #          },
        #     'broken': {'wap21', 'wap22'},
        # }}
        # c_contC = {"c_cont3": {
        #     'State': '0',
        #     'rote':
        #         {'rote1': {'wap31', 'wap32'},
        #          'rote2': {'wap32', 'wap33'},
        #          'rote3': {'wap33', 'wap34'},
        #          },
        #     'broken': {'wap31', 'wap32'},
        # }}

        c_cont1 = {'State': '0',
                   'rote':
                       {'rote1': ['wap31', 'wap32'],
                        'rote2': ['wap32', 'wap33'],
                        'rote3': ['wap33', 'wap34'],
                        },
                   'broken': ['wap31', 'wap32']
                   }

        # print(type(c_cont1))
        # c_cont = {"c_contA","c_contB","c_contC"}
        #
        # print(type(c_cont))
        # msg.Args = c_cont

        # msg.Args = c_cont1
        # msg.Args = {'c_cont1': 'c_contA', 'c_cont2': 'c_contB', 'c_cont3': 'c_contC'}

        # print(type(msg.Args))
        # print(type(msg.Args))

        # C - CONTからWCAの情報を受信
        # ↓
        # 複数個あるWCAの情報が揃うまで待機
        # ↓
        # 複数個あるWCAの状態をネットワークオペレータへ通知    Cognition
        # ↓
        # 改善が必要ならネットワークオペレータから制御命令
        # ↓
        # IoTアプリケーションプロバイダはIoTアプリケーションの要求を入力
        # ↓
        # Decisionは送られてきたアプリケーションの要求とWCAの状態をもとに経路制御命令を決める
        # ↓
        # OperationはどのC-CONTへ送信するか決める


        # msg.Args = c_cont1
        # msg.To = "Sensing"  # 宛先の変更
        # agt.send_message(msg, qos=0)  # メッセージ送信

        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = agt.name
        # msg.To = "Decision"
        # msg.To = "C_CONT_IF"
        msg.Action = "OUTPUT"
        # msg.TaskID = {"SENTENCE": data}
        # data = "a"
        msg.Args = c_cont1
        # msg.Args = {"SENTENCE": data,}
        # agt.send_message(msg, qos=0)
        print("A message was sent.")
        msg.To = "Sensing"
        # msg.Args = {"":""}
        agt.send_message(msg, qos=0)

        # if msg.From = "Operation":
        #     print("operation")
        # else:
        #     print("c-cont")


if __name__ == "__main__":
    print("===============================================================")
    print("OUTPUT CONSOLE")
    print("===============================================================")
    print("Exit Console : Ctrl-c")
    # エージェントの起動
    agt = ResourceConnectorAgent("C_CONT_IF", local=True)
