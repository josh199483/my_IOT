import paho.mqtt.client as mqtt
import time
import random
import sys
import logging

TOPIC = "MYTOPIC"
# 當與broker連接時會呼叫的callback
def on_connect(pahoClient, userdata, flags, rc):
    if rc==0:
        #client.connected_flag = True #set flag=True
        print("connected OK Returned code=",rc)
        pahoClient.subscribe(TOPIC)
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
def on_publish(pahoClient,userdata,mid):
    print("have published")
#有log時的callback
def on_log(pahoClient, userdata, level, buf):
    print("log: ",buf)
def on_disconnect(pahoClient, userdata,rc=0):
    print("disconnected")
    logging.debug("DisConnected result code "+str(rc))
    pahoClient.loop_stop()
    # 重新連線可能不能寫在這?因為這邊是當一斷線後做的事，或是一直嘗試重新連線直到連上為止
    # pahoClient.reconnect()

broker_address = "192.168.124.88"

print("create client")
mqttc = mqtt.Client("mqtt") #give it an id
#設定對應的callback
mqttc.on_connect = on_connect
mqttc.on_log = on_log
mqttc.on_publish = on_publish
mqttc.on_message = on_message
# mqttc.enable_logger(logger=logging.DEBUG)????
mqttc.on_disconnect = on_disconnect
try:
    mqttc.connect(broker_address)
except ConnectionRefusedError as e:
    print("connection failed "+str(e))
    #當沒有連線成功時，試著重新連線2次，此處該如何判斷從無連線到有連線就跳出迴圈?
    #for _ in range(2):
    #client.reconnect()


mqttc.loop_start()

print("connecting to ",broker_address)
# mqttc.subscribe("MYTOPIC")

while True:#client.connected_flag: #wait in loop
    try:
        print("in Main Loop")
        ran = random.randint(0, 99)
        mqttc.publish("MYTOPIC",ran)
        print("published")
        time.sleep(1)
    except:
        mqttc.disconnect()
        sys.exit()
# mqttc.loop_forever()

# mqttc.loop_stop()