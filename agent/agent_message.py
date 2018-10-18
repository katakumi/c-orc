# -*- coding: utf-8 -*-

import calendar
import datetime
import json


class AgentMessage:
    """
    エージェントメッセージ構成クラス
    """
    def __init__(self, json_text=None):
        self.Name = ""
        self.Type = "INFORM"
        self.Date = 0
        self.From = ""
        self.To = ""
        self.Action = ""
        self.Args = None
        self.Contents = None
        self.ContentLanguage = ""
        self.ErrorContents = ""
        self.Timeout = ""
        self.TimeLimit = ""
        self.Ack = ""
        self.Protocol = ""
        self.Strategy = ""
        self.ButFor = ""
        self.TaskID = ""
        self.ReplyTo = ""
        self.RepeatCount = ""
        self.TaskTimeout = ""
        self.SenderIP = ""
        self.SenderSite = ""
        self.Thru = ""

        if json_text is not None:
            self.parse(json_text)



    def to_json(self):
        self.Date = self.generate_unix_time()
        
        # Output Filter
        f = ['Type', 'Date', 'From', 'To', 'Action', 'Args', 'Contents']
        d = {k : v for k, v in filter(lambda t: t[0] in f, self.__dict__.items())} # [TODO]
        return json.dumps(d)
    
    
    def validate(self):
        pass

    def generate_unix_time(self):
        now = datetime.datetime.utcnow()
        ut = calendar.timegm(now.utctimetuple())
        # print("Unix time : {0}".format(ut))
        return ut


    def parse(self, json_text):
        j = json.loads(json_text)
        for k, v in j.items():
            self.__dict__[k] = v



if __name__ == "__main__":
    # for debug
    msg = AgentMessage()
    print(msg.to_json())

    json_sample = '{"Type": "", "Date": 1499368977, "From": "", "To": "", "Action": "", "Args": {"test-1": null}, "Contents": null}'
    t = msg.parse(json_sample)
    print(msg.__dict__)
    
