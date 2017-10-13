import paho.mqtt.client as mqtt #import the client1

def on_connect(client, userdata, flags, rc):
    if rc==0:
        # client.connected_flag = True #set flag=True
        print("connected OK Returned code=",rc)
        client.subscribe("MYTOPIC",1)
        print("subscribed topic")
    else:
        # client.connected_flag = False  # set flag=False
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, msg):
    print("this topic is:",msg.topic)
    print("this payload is:",str(msg.payload.decode('utf-8')))
    print("this qos is:",msg.qos)
broker_address="192.168.124.88"

client = mqtt.Client()
try:
    client.connect(broker_address)
except ConnectionRefusedError as e:
    print("connection failed "+str(e))
#當連上broker時的callback
client.on_connect = on_connect
#當接收到訊息時的callback
client.on_message = on_message

client.connect(broker_address) #connect to broker

client.loop_forever()
