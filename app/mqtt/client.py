import os
from paho.mqtt import client as mqtt_client
from dotenv import load_dotenv


class MqttClient(object):
    def __init__(self):
        load_dotenv(".env")
        self.broker = os.getenv('MQTT_BROKER')
        self.port = int(os.getenv('MQTT_PORT'))
        self.client = None
        self.client_id = os.getenv('MQTT_CLIENT_ID')

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        print(self.broker, self.port)
        client.connect(self.broker, self.port)
        self.client = client
        self.client.loop_start()
        self.client.loop_forever()

    def publish(self, topic, payload, **kwargs):
        result = self.client.publish(topic, payload)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{payload}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def subscribe(self, topic, call_back):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.client.subscribe(topic)
        self.client.on_message = call_back


mqtt_cli = MqttClient()
