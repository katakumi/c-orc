# -*- coding: utf-8 -*-
from agent.agent_message import AgentMessage

import paho.mqtt.client as mqtt
import ssl
import configparser


class BaseAgent:
    # Agent Actions
    ACTIONS = {
            #'TEST' : 'act_debug'
        }

    input_only = False
    local = False

    def load_settings(self):
        # Coterie設定の読み込み
        config = configparser.ConfigParser()
        config.read('settings.ini')

        self.coterie = config['SETTINGS']['CoterieName']
        self.topic = 'agent-space/coterie/' + self.coterie

        print("[LOG]", "Load Settings : Coterie - ", self.coterie)



    def connect(self):
        # Publisherと同様に v3.1.1を利用
        self.client = client = mqtt.Client(protocol=mqtt.MQTTv311)
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        # エージェント空間への接続
        # MQTTの設定
        if not self.local:
            self.host = 'sgnl.rcon.space'
            self.port = 443
            client.tls_set("agent_space.ca", cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1_2)
            client.tls_insecure_set(True)

        else:
            self.host = '127.0.0.1'
            self.port = 1883
        print(self.local)
        client.connect(self.host, port=self.port, keepalive=60)

        # 待ち受け状態にする
        if not self.input_only:
            client.loop_forever()

        print("[LOG] Network Access - OK")



    def reconnect(self):
        try:
            self.client.disconnect()
        finally:
            self.connect()


    def __init__(self, name, input_only=False, local=False):
        # エージェントの初期化
        self.name = name
        self.input_only = input_only
        self.local = local

        self.load_settings()
        self.connect()


    def on_connect(self, client, userdata, flags, respons_code):
        print('[LOG] MQTT status {0}'.format(respons_code))
        client.subscribe(self.topic, 2)
        
        msg = AgentMessage()
        msg.Type = "INFORM"
        msg.From = self.name
        msg.To = "ALL"
        msg.Action = "HELLO"
        msg.Args = ""
        #ここから使い
        msg.TaskName = ""
        msg.WCAs = ""
        msg.StartDate = ""
        msg.StartTime = ""
        msg.EndDate = ""
        msg.EndTime = ""
        client.publish(self.topic, msg.to_json(), 2)
        
    
    
    def on_message(self, client, userdata, msg):
        # AgentMessage型にパース
        data = msg.payload.decode("utf-8")
        agt_msg = AgentMessage(data)
        
        if agt_msg.To in (self.name, "ALL") and agt_msg.From != self.name:
#            print("\033[1;46m" + "[LOG] Received message '" + str(msg.payload) + "' on topic '"
#              + msg.topic + "' with QoS " + str(msg.qos) + "\033[1;m")

            self.receive_message(agt_msg)

        # キャッシュキューに登録
#        que.put(msg.payload.decode("utf-8"))


    def send_message(self, msg:AgentMessage, qos=2):
        if self.client._sock is None:
            self.client.disconnect()
            self.client.connect()

        self.client.publish(self.topic, msg.to_json(), qos)

    
    """
    for override
    """
    def receive_message(self, msg:AgentMessage):
        #print("[DEBUG-NEW]", msg.to_json())
        if msg.Action in self.ACTIONS:
            action_name = self.ACTIONS[msg.Action]
            try:
                method = getattr(self, action_name)
            except AttributeError:
                print("[ERROR]", action_name, "is nothing.")
            method(msg)
    
        
    # --- Properties ---
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


