import os
from paho.mqtt import client as mqtt_client
from dotenv import load_dotenv


def send_mqtt_msg(client_id, topic, payload):
    """
    发送mqtt消息. 需要以单独进/线程方式调用
    :param client_id:
    :param topic:
    :param payload:
    :return:
    """
    mqtt_cli = MQTT(client_id)
    mqtt_cli.connect_mqtt()
    mqtt_cli.publish(topic, payload)


def recv_mqtt_msg(client_id, topic, callback):
    """
    接收mqtt消息. 需要以单独进/线程方式调用
    :param client_id:
    :param topic:
    :param callback:
    :return:
    """
    mqtt_cli = MQTT(client_id)
    mqtt_cli.connect_mqtt()
    mqtt_cli.subscribe(topic, callback)


class MQTT(object):
    def __init__(self, client_id):
        load_dotenv(".env")
        self.broker = os.getenv('MQTT_BROKER', '127.0.0.1')
        self.port = int(os.getenv('MQTT_PORT'))
        self.client_id = os.getenv('MQTT_CLIENT_ID') + str(client_id)
        self.client = mqtt_client.Client(self.client_id)

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.client.on_connect = on_connect
        print(self.broker, self.port)
        self.client.connect(self.broker, self.port)

    def publish(self, topic, payload, **kwargs):
        result = self.client.publish(topic, payload)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send <{payload}> to topic <{topic}>")
        else:
            print(f"Failed to send message to topic {topic}")

    def subscribe(self, topic, callback):
        def on_message(client, userdata, msg):
            print(f"Received <{msg.payload.decode()}> from <{msg.topic}> topic")

        self.client.subscribe(topic)
        self.client.on_message = callback
        self.client.loop_forever()
