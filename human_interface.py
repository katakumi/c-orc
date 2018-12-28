from flask import Flask, render_template, request
import json
from agent.edge_agent import EdgeBaseAgent
from agent.agent_message import AgentMessage

app = Flask(__name__)
from datetime import datetime as dt


class ResourceConnectorAgent(EdgeBaseAgent):
    pass


@app.route('/', methods=['GET', 'POST'])
def a():
    if request.method == 'POST':
        name = request.form['app_name']
        print(name)
    return render_template("a.html")


@app.route('/wca')
def hello():
    return render_template("test1.html")


def act_replace(date0, time0):
    if date0.find("January") > 0:
        date = date0.replace("January,", "1")
    elif date0.find("February") > 0:
        date = date0.replace("February,", "2")
    elif date0.find("March") > 0:
        date = date0.replace("March,", "3")
    elif date0.find("April") > 0:
        date = date0.replace("April,", "4")
    elif date0.find("May") > 0:
        date = date0.replace("May,", "5")
    elif date0.find("June") > 0:
        date = date0.replace("June,", "6")
    elif date0.find("July") > 0:
        date = date0.replace("July,", "7")
    elif date0.find("August") > 0:
        date = date0.replace("August,", "8")
    elif date0.find("September") > 0:
        date = date0.replace("September,", "9")
    elif date0.find("October") > 0:
        date = date0.replace("October,", "10")
    elif date0.find("November") > 0:
        date = date0.replace("November,", "11")
    elif date0.find("December") > 0:
        date = date0.replace("December,", "12")

    time00 = date + " " + time0
    datetime = dt.strptime(time00, '%d %m %Y %H:%M')
    datetime_ts = datetime.timestamp()

    return datetime_ts


@app.route('/test2', methods=['POST', 'GET'])
def confirm():
    if request.method == 'POST':
        taskname = request.form['first_name']
        wcas = request.form['wcas']
        startdate = request.form['startdate']
        starttime = request.form['starttime']
        enddate = request.form['enddate']
        endtime = request.form['endtime']
        wap = request.form['wap']
        priority = request.form['priority']
        type = request.form['type']


        print(wap)

        start_unix = act_replace(startdate, starttime)
        print("Start Time unix ", start_unix)
        end_unix = act_replace(enddate, endtime)
        print("End Time unix ", end_unix)


        # 辞書型へ変換
        data = {"Task Name": taskname,
                "WCAs": wcas,
                "start_unix": start_unix,
                "end_unix": end_unix,
                "wap" : wap,
                "Priority": priority,
                "Type": type
                }
        print(data["start_unix"])
        print("aaaaa", data)

        # デバッグのために非表示
        # print(data)                     #辞書全ての表示
        # print (data["Start Date "])     #辞書内の特定のキーを出力
        # print(json.dumps(data, indent=2))

        # デバッグのために非表示
        # #辞書型→jsonへ
        # data1 = json.dumps(data)
        # print(data1)
        # #json→辞書型
        # data2 = json.loads(data1)
        # # print(json.dumps(data2, indent=2))
        # # print(data2)
        # print(data2)

        agt = ResourceConnectorAgent("INPUT")

        # SAMへ送信
        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = agt.name
        msg.Action = "OUTPUT"
        # msg.TaskID = {"SENTENCE": data}
        # data = "a"
        msg.Args = data
        print(msg.Args)
        # msg.Args = {"SENTENCE": data,}
        print("A message was sent.")
        # msg.To = "C_CONT_IF"
        # msg.Args = {"":""}
        msg.To = "Decision"
        # msg.To = "C_CONT_IF"
        agt.send_message(msg, qos=0)
        msg.To = "Cognition"
        agt.send_message(msg, qos=0)


        if start_unix < end_unix:
            print("ture1")
            return render_template("test2.html")
        elif start_unix > end_unix or start_unix == end_unix:
            print("false1")
            return render_template("error.html")



if __name__ == "__main__":
    app.run(debug=True)
