import paho.mqtt.client as mqtt
from PIL import Image
import io

TOPIC = "image"
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
    ##用open開啟的檔案有錯誤
    # with open("image.jpg",'w') as i:
    #     i.write(str(msg.payload))
    ##此方法可直接讀取bytes檔案
    image = Image.open(io.BytesIO(msg.payload))
    image.save("image.jpg")
    print("this topic is:",msg.topic)
    print("this payload is:",msg.payload)
    print("this qos is:",msg.qos)
def on_log(pahoClient, userdata, level, buf):
    print("log: ",buf)
broker_address="192.168.124.88"

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_log = on_log
mqttc.connect(broker_address)

mqttc.loop_forever()