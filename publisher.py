import paho.mqtt.client as mqtt
import time

MQTT_BROKER = "localhost"  # broker address
MQTT_PORT = 1883  # mqtt port
TOPIC = "test/code"
BACK_CHANNEL = "test/output"

cpp_code = """
#include <bits/stdc++.h>
using namespace std;
int main() {
int a=2;
int b=4;
    cout << "Hello, world!" << endl;
   cout << a + b << endl;
    return 0;
}
"""

def on_connect(client, userdata, flags, rc):
    print("Publisher connected with result code "+str(rc))
    publisher.subscribe(BACK_CHANNEL)
    print(f"Subsribed to {BACK_CHANNEL}")


def on_message(client, userdata, msg):
    print("Received acknowledgment from subscriber:")
    print(msg.payload.decode())

publisher = mqtt.Client("Publisher")

publisher.on_connect = on_connect
publisher.on_message = on_message

publisher.connect(MQTT_BROKER, MQTT_PORT, 60)
publisher.loop_start()


while True:
    publisher.publish(TOPIC, cpp_code)
    print(f"Code published\nWaiting for output")
    time.sleep(5)