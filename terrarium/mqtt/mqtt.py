import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.


# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
#client.on_message = on_message

try:
    client.connect("broker.emqx.io", 1883, 60)
except:
    print("connection failed")
    exit(1)  # Should quit or raise flag to quit or retry
# client.loop_start()
