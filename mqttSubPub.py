import paho.mqtt.client as mqtt
import time
import random
import sys
import logging

# 當與broker連接時會呼叫的callback
def on_connect(pahoClient, userdata, flags, rc):
    if rc==0:
        #client.connected_flag = True #set flag=True
        print("connected OK Returned code=",rc)
        client.subscribe("MYTOPIC")
        print("subscribed topic")
    else:
        #client.connected_flag = False  # set flag=False
        print("Bad connection Returned code=",rc)
# 當接受來自broker的訊息時
def on_message(pahoClient, userdata, msg):
    print("this topic is:",msg.topic)
    print("this payload is:",str(msg.payload.decode('utf-8')))
    print("this qos is:",msg.qos)
#當發布MQTT訊息時的callback
def on_publish(client,userdata,mid):
    print("have published")
#有log時的callback
def on_log(client, userdata, level, buf):
    print("log: ",buf)
broker_address = "192.168.124.88"

print("create client")
client = mqtt.Client("mqtt") #give it an id
#設定對應的callback
client.on_connect = on_connect
client.on_log = on_log
client.on_publish = on_publish
client.on_message = on_message
# client.enable_logger(logger=logging.DEBUG)????
try:
    client.connect(broker_address)
except ConnectionRefusedError as e:
    print("connection failed "+str(e))
    #當沒有連線成功時，試著重新連線2次，此處該如何判斷從無連線到有連線就跳出迴圈?
    #for _ in range(2):
    #client.reconnect()


client.loop_start()

print("connecting to ",broker_address)
# client.subscribe("MYTOPIC")

while True:#client.connected_flag: #wait in loop
    try:
        print("in Main Loop")
        ran = random.randint(0, 99)
        client.publish("MYTOPIC",ran)
        time.sleep(1)
    except:
        client.disconnect()
        sys.exit()
# client.loop_forever()

client.loop_stop()