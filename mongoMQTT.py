from pymongo import MongoClient
import paho.mqtt.client as mqtt
import logging
import json

client = MongoClient("mongodb://admin:pome@192.168.124.81:27017/pome")
db = client.pome

#測試RPI3發佈資料，本機訂閱資料，並寫進mongo資料庫
#這裡訂閱的資料以公司到機台設定組合而成
TOPIC = "#"
def on_connect(pahoClient, userdata, flags, rc):
    if rc==0:
        # client.connected_flag = True #set flag=True
        print("connected OK Returned code=",rc)
        pahoClient.subscribe(TOPIC,1)
        print("subscribed topic")
    else:
        # client.connected_flag = False  # set flag=False
        print("Bad connection Returned code=",rc)

def on_message(pahoClient, userdata, msg):
    print("this topic is:",msg.topic)
    print("this payload is:",str(msg.payload.decode('utf-8')))
    payload = json.loads(msg.payload)
    print(payload['t'])
    print("this qos is:",msg.qos)
    #
    toMongo(msg.topic,msg.payload)
#有log時的callback
def on_log(pahoClient, userdata, level, buf):
    print("log: ",buf)
def on_disconnect(pahoClient, userdata,rc=0):
    print("disconnected")
    logging.debug("DisConnected result code "+str(rc))
    # pahoClient.loop_stop()
def toMongo(topic,payload):
    #把對應的topic和payload寫進MongoDB
    TOPIC = topic
    PAYLOAD = json.loads(payload)
    timestamp = PAYLOAD['t']
    way = PAYLOAD['w']
    list = PAYLOAD['l']
    dict = {'topic':TOPIC,'timestamp': timestamp, 'way': way,'list': list}
    result = db.testMQTT.insert_one(dict)
    print(result.inserted_id)

broker_address="192.168.124.88"

mqttc = mqtt.Client()
#當連上broker時的callback
mqttc.on_connect = on_connect
#當接收到訊息時的callback
mqttc.on_message = on_message
mqttc.on_log = on_log

try:
    mqttc.connect(broker_address)
except ConnectionRefusedError as e:
    print("connection failed "+str(e))


mqttc.loop_forever()
