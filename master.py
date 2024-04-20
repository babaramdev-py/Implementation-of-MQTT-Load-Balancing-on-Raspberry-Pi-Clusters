import paho.mqtt.client as mqtt
import time
import queue

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_1 = "inputcode/node1"
TOPIC_2 = "inputcode/node2"
BACK_CHANNEL = "outputcode/master"

cpp_code = """
#include <iostream>
using namespace std;
int main() {
    int a=0;
    int b=1;
    cout << "Response From Child Node One" << endl;
    cout << a + b << endl;
    return 0;
}
"""
cpp_code_two = """
#include <iostream>
using namespace std;
int main() {
    int a=0;
    int b=2;
    cout << "Response From Child Node Two" << endl;
    cout << a + b << endl;
    return 0;
}
"""

code_queue = queue.Queue()
code_queue.put(cpp_code)
code_queue.put(cpp_code_two)

def on_connect(client, userdata, flags, rc):
    print("Publisher connected with result code "+str(rc))
    publisher.subscribe(BACK_CHANNEL)
    print(f"Subscribed to {BACK_CHANNEL}")

def on_message(client, userdata, msg):
    print(f"Received acknowledgment from Child Node")
    print(msg.payload.decode())

publisher = mqtt.Client("Master_Node")
publisher.on_connect = on_connect
publisher.on_message = on_message
publisher.connect(MQTT_BROKER, MQTT_PORT, 60)
publisher.loop_start()

while True:
    time.sleep(0.5)  
    publisher.publish(TOPIC_1, cpp_code)
    print(f"Code published for {TOPIC_1}. Waiting for output...\n")
    publisher.publish(TOPIC_2, cpp_code_two)
    print(f"Code published for {TOPIC_2}. Waiting for output...\n")
    time.sleep(0.5)
